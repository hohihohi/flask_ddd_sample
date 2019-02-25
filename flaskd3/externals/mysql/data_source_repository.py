from flaskd3 import domains
from flaskd3.externals.mysql import orm
from datetime import datetime
from sqlalchemy.exc import IntegrityError, InvalidRequestError, ObjectNotExecutableError

DataSource_Required = ['user_id']


class DataSourceRepository(domains.DataSourceRepositoryIF):

    def __init__(self, session):
        # super()
        self.session = session  # set session to connect database

    @classmethod
    def _record_to_model(cls, record):
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
                          'data_type',
                          'region',
                          'id',
                          'created_at',
                          'updated_at',
                          'deleted_at']
                         ):
            raise Exception("Fail to convert record to model: datasource")
        return domains.DataSource(
            record.user_id,
            record.name,
            record.data_type,
            record.region,
            record.id,
            None,
            record.created_at,
            record.updated_at,
            record.deleted_at
        )

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
            return DataSourceRepository._record_to_model(record)
        except Exception:
            raise domains.NotFoundError(param=data_id)

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
            return DataSourceRepository._record_to_model(record)
        except Exception:
            raise domains.NotFoundError(param=name)

    # find data sources by user id from database. This method should return data sources object or None
    def find_by_user_id(self, user_id):
        try:
            record = self.session \
                .query(orm.Datum) \
                .filter_by(user_id=user_id) \
                .filter(orm.Datum.deleted_at > datetime.now())
            if record is None:
                return None
            # TODO: 複数返ってくるはず
            return DataSourceRepository._record_to_model(record)
        except Exception:
            raise domains.NotFoundError(param=user_id)

    # save data source with the object to database. This method should return saved data source object or error
    # https://docs.sqlalchemy.org/en/latest/orm/session_basics.html
    def save(self, data_source):
        # NOTE: Call ObjectRepository.save method before call this method
        def _data_source_to_records(ds):
            data_source_copied = ds.copy()
            records = orm.Datum(
                user_id=data_source_copied.user_id,
                object_id=data_source_copied.object.id,
                name=data_source_copied.name,
                data_type=data_source_copied.data_type.name.lower(),
                deleted_at=data_source_copied.deleted_at
            )
            return records
        try:
            records = _data_source_to_records(data_source)
            print('records:', records)
            # save record
            self.session.add(records)
            # reflect database
            self.session.commit()
            # TODO: update id, created_at, updated_at
            saved = self.session.query(orm.Datum) \
                .filter_by(name=data_source.name, user_id=data_source.user_id) \
                .first()
            self.session.flush()
            return DataSourceRepository._record_to_model(saved)
        except IntegrityError as e:
            if 'Duplicate entry' in str(e):
                raise Exception('Invalid parameter duplicate error occurred: DataSource')
            raise e

    # delete data source with the object from database. This method should return deleted data source object or error
    # https://docs.sqlalchemy.org/en/latest/core/dml.html
    def delete(self, data_source):
        # NOTE: Call ObjectRepository.delete method after call this method
        def _data_source_to_record(ds):
            data_source_dict = ds.copy().__dict__
            return orm.Datum(data_source_dict)
        try:
            record = _data_source_to_record(data_source)
            # find target data
            found_data = self.session.query(orm.Datum)\
                .filter_by(id=record.id)\
                .first()
            # TODO: handle found_data is None
            self.session.delete(found_data)
            # reflect database(commit should be called when update, insert, delete)
            self.session.commit()
            deleted = self.session.query(orm.Datum) \
                .filter_by(id=found_data.id) \
                .first()
            self.session.flush()
            return DataSourceRepository._record_to_model(deleted)
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
            return DataSourceRepository._record_to_model(updated)
        except (InvalidRequestError, ObjectNotExecutableError) as e:
            raise Exception(f'Cannot update {data_source.name} datasource: {str(e)}')
