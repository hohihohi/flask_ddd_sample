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
    def _extract_only_column_name(cls, table_name, columns):
        column_names = []
        delete_initial_chars = len(table_name) + 1  # table_name.***
        for column in columns:
            column_names.append(str(column)[delete_initial_chars:])
        column_names.sort()
        return column_names

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
            return ObjectRepository._bucket_record_to_model(record)
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

    def _should_delete_bucket(self, bucket_id):
        # find objects by bucket_id
        try:
            records = self.session \
                .query(orm.Object) \
                .filter_by(bucket_id=bucket_id) \
                .filter(orm.Object.deleted_at > datetime.now())
            if not records:
                return True
            record_list = [self._object_record_to_model(record) for record in records]
            if len(record_list) == 0:
                return True
            return False
        except Exception:
            # TODO: logger
            return False

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
            return domains.NotFoundError(param=object_id)

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
            return domains.NotFoundError(param=name)

    # find object sources by user id from database. This method should return object or None
    def find_by_user_id(self, user_id):
        try:
            records = self.session \
                .query(orm.Object) \
                .filter_by(user_id=user_id) \
                .filter(orm.Object.deleted_at > datetime.now())
            if not records:
                return []
            record_list = [self._object_record_to_model(record) for record in records]
            return record_list
        except Exception:
            return domains.NotFoundError(param=user_id)

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
                return Exception('Invalid parameter duplicate error occurred: Object')
            return e

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
            # save record
            self.session.add(record)
            # reflect database
            self.session.commit()
            # TODO: update id, created_at, updated_at
            saved = self.session.query(orm.Bucket) \
                .filter_by(name=bucket.name, user_id=bucket.user_id) \
                .first()
            self.session.flush()
            # return ObjectRepository._bucket_record_to_model(saved)
            saved_bucket = ObjectRepository._bucket_record_to_model(saved)
            self._find_bucket_by_id(saved_bucket.id)
            return saved_bucket
        except IntegrityError as e:
            if 'Duplicate entry' in str(e):
                return Exception('Invalid parameter duplicate error occurred: Bucket')
            return e

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
                created_at=obj.created_at,
                updated_at=obj.updated_at
            )
        try:
            record = _object_to_record(ob)
            # find target data
            found_obj = self.session.query(orm.Object) \
                .filter_by(id=record.id) \
                .first()
            if found_obj is None:
                self.session.flush()
                return Exception(f'Cannot delete object because object was not found: {ob.name}')
            self.session.delete(found_obj)
            # reflect database(commit should be called when update, insert, delete)
            self.session.commit()
            self.session.flush()
            found_obj.deleted_at = datetime.now()
            return self._object_record_to_model(found_obj)
        except (InvalidRequestError, ObjectNotExecutableError) as e:
            return Exception(f'Cannot delete {ob.name} object: {str(e)}')

    # delete bucket source from database. This method should return deleted bucket or error
    def delete_bucket(self, bucket):
        def _bucket_to_records(b):
            return orm.Bucket(
                id=b.id,
                user_id=b.user_id,
                name=b.name,
                region=b.region,
                created_at=b.created_at,
                updated_at=b.updated_at
            )
        # delete bucket if it is not used now
        if self._should_delete_bucket(bucket.id):
            del_bucket = self._find_bucket_by_id(bucket.id)
            try:
                record = _bucket_to_records(del_bucket)
                # find target data
                found_bucket = self.session.query(orm.Bucket) \
                    .filter_by(id=record.id) \
                    .first()
                if found_bucket is None:
                    self.session.flush()
                    # TODO: this error is critical !! but don't stop application
                    return Exception(f'Cannot delete object because bucket was not found: {bucket.name}')
                self.session.delete(found_bucket)
                self.session.commit()
                self.session.flush()
                found_bucket.deleted_at = datetime.now()
                return self._bucket_record_to_model(found_bucket)
            except (InvalidRequestError, ObjectNotExecutableError) as e:
                return Exception(f'Cannot delete {bucket.name} bucket: {str(e)}')
        self.session.flush()
        return Exception(f'Cannot delete bucket because some objects use it: {bucket.name}')

    # update data source with the object to database. This method should return updated data source object or error
    def update(self, ob):
        def _object_to_record(obj):
            return orm.Object(
                id=obj.id,
                user_id=obj.user_id,
                name=obj.name,
                region=obj.region,
                version=obj.version,
                bucket_id=obj.bucket.id,
                created_at=obj.created_at,
                updated_at=obj.updated_at,
                deleted_at=obj.deleted_at
            )
        try:
            record = _object_to_record(ob)
            # find target data
            found_obj = self.session.query(orm.Object) \
                .filter_by(id=record.id) \
                .first()
            if found_obj is None:
                self.session.flush()
                return Exception(f'Cannot update object because object was not found: {ob.name}')
            self.session.merge(record)
            self.session.commit()
            updated = self.session.query(orm.Object) \
                .filter_by(id=record.id) \
                .first()
            self.session.flush()
            return self._object_record_to_model(updated)
        except IntegrityError as e:
            if 'Duplicate entry' in str(e):
                return Exception('Invalid parameter duplicate error occurred: Object')
            return e
