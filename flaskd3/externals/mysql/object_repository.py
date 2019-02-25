from flaskd3 import domains
from flaskd3.externals.mysql import orm
from datetime import datetime
from sqlalchemy.exc import IntegrityError, InvalidRequestError, ObjectNotExecutableError

DataSource_Required = ['user_id']


class ObjectRepository(domains.ObjectRepositoryIF):

    def __init__(self, session):
        # super()
        self.session = session  # set session to connect database

    @classmethod
    def _bucket_record_to_model(cls, record):
        # judge whether dictionary includes the necessary parameters or not
        def _includes(dic, requires):
            for require in requires:
                if require not in dic.keys():
                    return False
            return True
        # guard
        if not _includes(record,
                         ['user_id',
                          'name',
                          'region',
                          'id',
                          'created_at',
                          'updated_at',
                          'deleted_at']
                         ):
            raise Exception("Fail to convert record to model: bucket")
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
            return ObjectRepository._bucket_record_to_model(bucket_id)
        except Exception:
            raise domains.NotFoundError(param=bucket_id)

    def _object_record_to_model(self, record):
        # judge whether dictionary includes the necessary parameters or not
        def _includes(dic, requires):
            for require in requires:
                if require not in dic.keys():
                    return False
            return True
        # guard
        if not _includes(record,
                         ['user_id',
                          'name',
                          'region',
                          'version',
                          'bucket_id',
                          'id',
                          'created_at',
                          'updated_at',
                          'deleted_at']
                         ):
            raise Exception("Fail to convert record to model: datasource")

        # find bucket
        bucket = self._find_bucket_by_id(record.bucket_id)
        return domains.Object(
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

    # find object source by id from database. This method should return object or None
    def find_by_id(self, object_id):
        try:
            record = self.session \
                .query(orm.Object) \
                .filter_by(id=object_id) \
                .filter(orm.Object.deleted_at > datetime.now()) \
                .first()
            if record is None:
                return None
            return self._object_record_to_model(record)
        except Exception:
            raise domains.NotFoundError(param=object_id)

    # find object source by name from database. This method should return object or None
    def find_by_name(self, name):
        try:
            record = self.session \
                .query(orm.Object) \
                .filter_by(name=name) \
                .filter(orm.Object.deleted_at > datetime.now()) \
                .first()
            if record is None:
                return None
            return self._object_record_to_model(record)
        except Exception:
            raise domains.NotFoundError(param=name)

    # find object sources by user id from database. This method should return object or None
    def find_by_user_id(self, user_id):
        try:
            record = self.session \
                .query(orm.Object) \
                .filter_by(user_id=user_id) \
                .filter(orm.Object.deleted_at > datetime.now())
            if record is None:
                return None
            # TODO: 複数返ってくるはず
            return self._object_record_to_model(record)
        except Exception:
            raise domains.NotFoundError(param=user_id)

    # save object source to database. This method should return saved object or error
    # https://docs.sqlalchemy.org/en/latest/orm/session_basics.html
    def save(self, ob):
        def _object_to_records(obj):
            return orm.Object(
                user_id=obj.user_id,
                name=obj.name,
                region=obj.region,
                version=obj.version,
                bucket_id=obj.bucket.id,
                deleted_at=obj.deleted_at
            )
        try:
            record = _object_to_records(ob)
            print('record:', record)
            # save record
            self.session.add(record)
            # reflect database
            self.session.commit()
            # TODO: update id, created_at, updated_at
            saved = self.session.query(orm.Object) \
                .filter_by(name=ob.name, user_id=ob.user_id) \
                .first()
            self.session.flush()
            return self._object_record_to_model(saved)
        except IntegrityError as e:
            if 'Duplicate entry' in str(e):
                raise Exception('Invalid parameter duplicate error occurred: Object')
            raise e

    # save bucket source database. This method should return saved bucket or error
    def save_bucket(self, bucket):
        # NOTE: Call ObjectRepository.save method before call this method
        def _bucket_to_records(b):
            return orm.Bucket(
                user_id=b.user_id,
                name=b.name,
                region=b.region,
                deleted_at=b.deleted_at
            )
        try:
            record = _bucket_to_records(bucket)
            print('record:', record)
            # save record
            self.session.add(record)
            # reflect database
            self.session.commit()
            # TODO: update id, created_at, updated_at
            saved = self.session.query(orm.Datum) \
                .filter_by(name=bucket.name, user_id=bucket.user_id) \
                .first()
            self.session.flush()
            return ObjectRepository._bucket_record_to_model(saved)
        except IntegrityError as e:
            if 'Duplicate entry' in str(e):
                raise Exception('Invalid parameter duplicate error occurred: Bucket')
            raise e

    # delete data source with the object from database. This method should return deleted data source object or error
    # https://docs.sqlalchemy.org/en/latest/core/dml.html
    def delete(self, ob):
        # NOTE: Call ObjectRepository.delete method after call this method
        def _object_to_record(obj):
            return orm.Object(
                id=obj.id,
                user_id=obj.user_id,
                name=obj.name,
                region=obj.region,
                version=obj.version,
                bucket_id=obj.bucket.id,
                created_at=obj.bucket.created_at,
                updated_at=obj.bucket.updated_at
            )
        try:
            record = _object_to_record(ob)
            # find target data
            found_data = self.session.query(orm.Object) \
                .filter_by(id=record.id) \
                .first()
            # TODO: handle found_data is None
            self.session.delete(found_data)
            # reflect database(commit should be called when update, insert, delete)
            self.session.commit()
            deleted = self.session.query(orm.Object) \
                .filter_by(id=found_data.id) \
                .first()
            self.session.flush()
            # TODO: Delete bucket

            return self._object_record_to_model(deleted)
        except (InvalidRequestError, ObjectNotExecutableError) as e:
            raise Exception(f'Cannot delete {data_source.name} datasource: {str(e)}')

    # update data source with the object to database. This method should return updated data source object or error
    def update(self, data_source):
        def _data_source_to_record(ds):
            data_source_dict = ds.copy().__dict__
            del data_source_dict['updated_at']
            return orm.Datum(data_source_dict)
        try:
            record = _data_source_to_record(data_source)
            # find target data
            found_data = self.session.query(orm.Datum) \
                .filter_by(id=record.id) \
                .first()
            # TODO: handle found_data is None
            self.session.merge(record)
            self.session.commit()
            updated = self.session.query(orm.Datum) \
                .filter_by(id=found_data.id) \
                .first()
            self.session.flush()
            return self._object_record_to_model(updated)
        except (InvalidRequestError, ObjectNotExecutableError) as e:
            raise Exception(f'Cannot update {data_source.name} datasource: {str(e)}')
