from flaskd3 import domains
from flaskd3.externals.mysql import orm
from datetime import datetime
from sqlalchemy.exc import IntegrityError

DataSource_Required = ['user_id']


class DataSourceRepository(domains.DataSourceRepositoryIF):

    def __init__(self, session):
        super()
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
    def find_by_id(self, id):
        try:
            record = self.session\
                .query(orm.Datum)\
                .filter_by(id=id)\
                .filter(orm.Datum.deleted_at > datetime.now())\
                .first()
            if record is None:
                return None
            return DataSourceRepository._record_to_model(record)
        except Exception:
            raise domains.NotFoundError(param=id)

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
        pass

    # save data source with the object to database. This method should return saved data source object or error
    def save(self, data_source):
        def _data_source_to_record(ds):
            data_source_dict = ds.copy().__dict__
            del data_source_dict['id']
            del data_source_dict['created_at']
            del data_source_dict['updated_at']
            return orm.Datum(data_source_dict)
        try:
            record = _data_source_to_record(data_source).serialize()
            self.session.add(record)
            self.session.flush()
            return DataSourceRepository._record_to_model(record)
        except IntegrityError as e:
            if 'Duplicate entry' in str(e):
                raise Exception("Invalid parameter duplicate error occurred: DataSource")
            raise e

    # delete data source with the object from database. This method should return deleted data source object or error
    def delete(self, data_source):
        pass

    # update data source with the object to database. This method should return updated data source object or error
    def update(self, data_source):
        pass
