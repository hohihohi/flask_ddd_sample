from flaskd3.externals.mysql import MySQLClient, orm
from flaskd3.domains import DataSource, DataObject, Bucket
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


##############
# test param #
##############
@pytest.fixture(scope='module')
def valid_data_source():
    return DataSource(
        'abc12345',
        'test_data_source',
        'raw',
        'jp-east-1'
    )


@pytest.fixture(scope='module')
def valid_object():
    return DataObject(
        'abc12345',
        'test_data_source',  # object name == data source name
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
def data_source_assertions(expect, actual):
    assert expect.id == actual.id
    assert expect.user_id == actual.user_id
    assert expect.name == actual.name
    object_assertions(expect.object, actual.object)
    assert expect.data_type == actual.data_type
    assert expect.created_at <= actual.created_at
    assert expect.updated_at <= actual.updated_at
    assert expect.deleted_at >= actual.updated_at


def data_source_list_assertions(expect, actual):
    assert len(expect) == len(actual)
    expect_sorted = sort_data_source_list_by_id(expect)
    actual_sorted = sort_data_source_list_by_id(actual)
    for i in range(len(expect_sorted)):
        data_source_assertions(expect_sorted[i], actual_sorted[i])


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


def sort_data_source_list_by_id(data_source_list):
    return sorted(data_source_list, key=lambda ds: ds.id)


def delete_record_from_database(session):
    session.query(orm.Datum).delete()
    session.query(orm.Object).delete()
    session.query(orm.Bucket).delete()
    session.commit()
