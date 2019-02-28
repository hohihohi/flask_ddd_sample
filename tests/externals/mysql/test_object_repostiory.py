from flaskd3.externals.mysql import ObjectRepository, MySQLClient, orm
from flaskd3.domains import DataObject, Bucket
import pytest


###############
# pre process #
###############
@pytest.fixture(scope='function')
def ormapper():
    valid_param = {
        'user_name': 'flaskd3',
        'password': 'flaskd3',
        'host_ip': 'mysql',
        'db_name': 'flaskd3'
    }
    return MySQLClient(
        valid_param['user_name'],
        valid_param['password'],
        valid_param['host_ip'],
        valid_param['db_name']
    )


@pytest.fixture(scope='function')
def clear_database():
    pass


##############
# test param #
##############
@pytest.fixture(scope='module')
def valid_object():
    return DataObject(
        'abc12345',
        'test_object',
        'jp-east-1',
    )

@pytest.fixture(scope='module')
def valid_bucket():
    return Bucket(
        'abc12345',
        'test_bucket',
        'jp-east-1',
    )


########
# util #
########
def object_assertions(expect, actual):
    assert expect.id == actual.id
    assert expect.user_id == actual.user_id
    assert expect.name == actual.name
    assert expect.region == actual.region
    assert expect.version == actual.version
    bucket_assertions(expect.bucket, actual.bucket)
    assert expect.created_at <= actual.created_at
    assert expect.updated_at <= actual.updated_at
    assert expect.deleted_at >= actual.updated_at


def object_list_assertions(expect, actual):
    assert len(expect) == len(actual)
    expect_sorted = sort_object_list_by_id(expect)
    actual_sorted = sort_object_list_by_id(actual)
    for i in range(len(expect_sorted)):
        object_assertions(expect_sorted[i], actual_sorted[i])


def bucket_assertions(expect, actual):
    assert expect.id == actual.id
    assert expect.user_id == actual.user_id
    assert expect.name == actual.name
    assert expect.region == actual.region
    assert expect.created_at <= actual.created_at
    assert expect.updated_at <= actual.updated_at
    assert expect.deleted_at >= actual.deleted_at


def sort_object_list_by_id(object_list):
    return sorted(object_list, key=lambda o: o.id)


def _delete_record_from_database(session):
    session.query(orm.Object).delete()
    session.query(orm.Bucket).delete()
    session.commit()


########
# test #
########
def test_find_by_id(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        _delete_record_from_database(session)
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
        _delete_record_from_database(session)
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
        _delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj_1 = valid_object.copy()
        obj_1.bucket = bucket
        obj_2 = valid_object.copy()
        obj_2.name = "test_object2"
        obj_2.bucket = bucket
        saved_1 = object_repository.save(obj_1)
        saved_2 = object_repository.save(obj_2)
        expect = [saved_2, saved_1]
        # call method to test
        actual = object_repository.find_by_user_id(valid_object.user_id)
        object_list_assertions(expect, actual)


def test_save(ormapper, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        _delete_record_from_database(session)
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
        _delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj_1 = valid_object.copy()
        obj_1.bucket = bucket
        obj_2 = valid_object.copy()
        obj_2.bucket = bucket
        expect = 'Invalid parameter duplicate error occurred: Object'
        try:
            # call method to test
            _ = object_repository.save(obj_1)
            _ = object_repository.save(obj_2)
        except Exception:
            assert expect == Exception.message


def test_save_bucket(ormapper, valid_bucket):
    with ormapper.create_session() as session:
        _delete_record_from_database(session)
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
        _delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        expect = 'Invalid parameter duplicate error occurred: Bucket'
        try:
            # call method to test
            _ = object_repository.save_bucket(valid_bucket)
            _ = object_repository.save_bucket(valid_bucket)
        except Exception:
            assert expect == Exception.message
