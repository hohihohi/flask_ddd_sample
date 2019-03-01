from flaskd3.externals.mysql import ObjectRepository
from tests.externals.mysql import *


def test_find_by_id(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        expect = object_repository.save(obj)
        # call method to test
        actual = object_repository.find_by_id(expect.id)
        object_assertions(expect, actual)


def test_find_by_name(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        expect = object_repository.save(obj)
        # call method to test
        actual = object_repository.find_by_name(expect.name)
        object_assertions(expect, actual)


def test_find_by_user_id(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj_1 = valid_object.copy()
        obj_1.bucket = bucket
        obj_2 = valid_object.copy()
        obj_2.name = 'test_data_source2'
        obj_2.bucket = bucket
        saved_1 = object_repository.save(obj_1)
        saved_2 = object_repository.save(obj_2)
        expect = [saved_2, saved_1]
        # call method to test
        actual = object_repository.find_by_user_id(valid_object.user_id)
        object_list_assertions(expect, actual)


def test_save(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        expect = valid_object.copy()
        expect.bucket = bucket
        # call method to test
        actual = object_repository.save(expect)
        assert actual.id is not None and actual.id >= 0
        assert expect.user_id == actual.user_id
        assert expect.name == actual.name
        assert expect.region == actual.region
        assert expect.version == actual.version
        bucket_assertions(expect.bucket, actual.bucket)
        assert expect.created_at < actual.created_at
        assert expect.updated_at < actual.updated_at


def test_save_with_duplicate_error(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj_1 = valid_object.copy()
        obj_1.bucket = bucket
        obj_2 = valid_object.copy()
        obj_2.bucket = bucket
        expect = 'Invalid parameter duplicate error occurred: Object'
        # call method to test
        _ = object_repository.save(obj_1)
        actual = object_repository.save(obj_2)
        assert expect == str(actual)


def test_save_bucket(ormapper, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        expect = valid_bucket.copy()
        # call method to test
        actual = object_repository.save_bucket(valid_bucket)
        assert actual.id is not None and actual.id >= 0
        assert expect.user_id == actual.user_id
        assert expect.name == actual.name
        assert expect.region == actual.region
        assert expect.created_at < actual.created_at
        assert expect.updated_at < actual.updated_at


def test_save_bucket_with_duplicate_error(ormapper, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        expect = 'Invalid parameter duplicate error occurred: Bucket'
        # call method to test
        _ = object_repository.save_bucket(valid_bucket)
        actual = object_repository.save_bucket(valid_bucket)
        assert expect == str(actual)


def test_delete(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        expect = object_repository.save(obj)
        # call method to test
        actual = object_repository.delete(expect)
        object_assertions(expect, actual)


def test_delete_with_non_exist_object(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        # call method to test
        expect = f'Cannot delete object because it was not found: {obj.name}'
        actual = object_repository.delete(obj)
        assert expect == str(actual)


def test_delete_bucket(ormapper, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        expect = object_repository.save_bucket(valid_bucket)
        # call method to test
        actual = object_repository.delete_bucket(expect)
        bucket_assertions(expect, actual)


def test_delete_bucket_used_some_objects(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        _ = object_repository.save(obj)
        # call method to test
        expect = f'Cannot delete bucket because some objects use it: {bucket.name}'
        actual = object_repository.delete_bucket(bucket)
        assert expect == str(actual)


def test_update(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        expect = object_repository.save(obj)
        expect.name = 'update_object'
        # call method to test
        actual = object_repository.update(expect)
        object_assertions(expect, actual)


def test_update_with_unique_error(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj_1 = valid_object.copy()
        obj_1.bucket = bucket
        obj_2 = valid_object.copy()
        obj_2.bucket = bucket
        obj_2.name = 'test_data_source2'
        saved_1 = object_repository.save(obj_1)
        saved_2 = object_repository.save(obj_2)
        # call method to test
        saved_2.name = saved_1.name
        expect = 'Invalid parameter duplicate error occurred: Object'
        actual = object_repository.update(saved_2)
        assert expect == str(actual)


def test_update_with_non_exist_object(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        # call method to test
        expect = f'Cannot update object because it was not found: {obj.name}'
        actual = object_repository.update(obj)
        assert expect == str(actual)
