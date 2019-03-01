from flaskd3 import domains
from flaskd3.externals.mysql import orm
from datetime import datetime
from sqlalchemy.exc import IntegrityError, InvalidRequestError, ObjectNotExecutableError


# FIXME: this class has anti-pattern, it will be refactored by repository pattern
class DataSourceRepository(domains.DataSourceRepositoryIF):

    def __init__(self, session):
        self.session = session  # set session to connect database

    @classmethod
    def _bucket_record_to_model(cls, record):
        return domains.Bucket(
            record.user_id,
            record.name,
            record.region,
            record.id,
            record.created_at,
            record.updated_at,
            record.deleted_at
        )

    def _find_bucket_by_id(self, bucket_id):
        try:
            record = self.session \
                .query(orm.Bucket) \
                .filter_by(id=bucket_id) \
                .filter(orm.Bucket.deleted_at > datetime.now()) \
                .first()
            if record is None:
                return None
            return DataSourceRepository._bucket_record_to_model(record)
        except Exception:
            return domains.NotFoundError(param='Bucket ID', raw=bucket_id)

    def _object_record_to_model(self, record):
        # find bucket
        bucket = self._find_bucket_by_id(record.bucket_id)
        return domains.DataObject(
            record.user_id,
            record.name,
            record.region,
            record.id,
            record.version,
            bucket,
            record.created_at,
            record.updated_at,
            record.deleted_at
        )

    def _find_object_by_id(self, object_id):
        try:
            record = self.session \
                .query(orm.Object) \
                .filter_by(id=object_id) \
                .filter(orm.Bucket.deleted_at > datetime.now()) \
                .first()
            if record is None:
                return None
            return self._object_record_to_model(record)
        except Exception:
            return domains.NotFoundError(param='Object ID', raw=object_id)

    def _datasource_record_to_model(self, record):
        ob = self._find_object_by_id(record.object_id)
        # TODO: I want to set object directly
        ds = domains.DataSource(
            record.user_id,
            record.name,
            record.data_type,
            ob.region,
            record.id,
            None,
            record.created_at,
            record.updated_at,
            record.deleted_at
        )
        ds.object = ob
        return ds

    # find data source by id from database. This method should return data source object or None
    def find_by_id(self, data_id):
        try:
            record = self.session\
                .query(orm.Datum)\
                .filter_by(id=data_id)\
                .filter(orm.Datum.deleted_at > datetime.now())\
                .first()
            if record is None:
                return None
            return self._datasource_record_to_model(record)
        except Exception:
            return domains.NotFoundError(param=data_id)

    # find data source by name from database. This method should return data source object or None
    def find_by_name(self, name):
        try:
            record = self.session\
                .query(orm.Datum)\
                .filter_by(name=name)\
                .filter(orm.Datum.deleted_at > datetime.now())\
                .first()
            if record is None:
                return None
            return self._datasource_record_to_model(record)
        except Exception:
            return domains.NotFoundError(param=name)

    # find data sources by user id from database. This method should return data sources object or None
    def find_by_user_id(self, user_id):
        try:
            records = self.session \
                .query(orm.Datum) \
                .filter_by(user_id=user_id) \
                .filter(orm.Datum.deleted_at > datetime.now())
            if not records:
                return []
            record_list = [self._datasource_record_to_model(record) for record in records]
            return record_list
        except Exception:
            return domains.NotFoundError(param=user_id)

    # save data source with the object to database. This method should return saved data source object or error
    # https://docs.sqlalchemy.org/en/latest/orm/session_basics.html
    def save(self, data_source):
        # NOTE: Call ObjectRepository.save method before call this method
        def _data_source_to_record(ds):
            return orm.Datum(
                user_id=ds.user_id,
                name=ds.name,
                data_type=ds.data_type.name.lower(),
                object_id=ds.object.id,
                deleted_at=ds.deleted_at
            )
        try:
            record = _data_source_to_record(data_source)
            # save record
            self.session.add(record)
            # reflect database
            self.session.commit()
            # TODO: update id, created_at, updated_at
            saved = self.session.query(orm.Datum) \
                .filter_by(name=data_source.name, user_id=data_source.user_id) \
                .first()
            self.session.flush()
            return self._datasource_record_to_model(saved)
        except IntegrityError as e:
            if 'Duplicate entry' in str(e):
                return Exception('Invalid parameter duplicate error occurred: DataSource')
            return e

    # delete data source with the object from database. This method should return deleted data source object or error
    # https://docs.sqlalchemy.org/en/latest/core/dml.html
    def delete(self, data_source):
        # NOTE: Call ObjectRepository.delete method after call this method
        def _data_source_to_record(ds):
            return orm.Datum(
                id=ds.id,
                user_id=ds.user_id,
                name=ds.name,
                data_type=ds.data_type.name.lower(),
                object_id=ds.object.id,
                created_at=ds.created_at,
                updated_at=ds.updated_at
            )
        try:
            record = _data_source_to_record(data_source)
            # find target data
            found_data = self.session.query(orm.Datum)\
                .filter_by(id=record.id)\
                .first()
            if found_data is None:
                self.session.flush()
                return Exception(f'Cannot delete data source because it was not found: {data_source.name}')
            self.session.delete(found_data)
            # reflect database(commit should be called when update, insert, delete)
            self.session.commit()
            self.session.flush()
            found_data.deleted_at = datetime.now()
            return self._datasource_record_to_model(found_data)
        except (InvalidRequestError, ObjectNotExecutableError) as e:
            return Exception(f'Cannot delete {data_source.name} datasource: {str(e)}')

    # update data source with the object to database. This method should return updated data source object or error
    def update(self, data_source):
        def _data_source_to_record(ds):
            return orm.Datum(
                id=ds.id,
                user_id=ds.user_id,
                name=ds.name,
                data_type=ds.data_type.name.lower(),
                object_id=ds.object.id,
                created_at=ds.created_at,
                updated_at=ds.updated_at,
                deleted_at=ds.deleted_at,
            )
        try:
            record = _data_source_to_record(data_source)
            # find target data
            found_data = self.session.query(orm.Datum) \
                .filter_by(id=record.id) \
                .first()
            if found_data is None:
                self.session.flush()
                return Exception(f'Cannot update data source because it was not found: {data_source.name}')
            self.session.merge(record)
            self.session.commit()
            updated = self.session.query(orm.Datum) \
                .filter_by(id=found_data.id) \
                .first()
            self.session.flush()
            return self._datasource_record_to_model(updated)
        except IntegrityError as e:
            if 'Duplicate entry' in str(e):
                return Exception('Invalid parameter duplicate error occurred: DataSource')
            return e
