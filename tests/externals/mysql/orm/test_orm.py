from flaskd3.externals.mysql.orm import MySQLClient
from sqlalchemy.orm.scoping import scoped_session


#########
# param #
#########
valid_param = {
    'user_name': 'flaskd3',
    'password': 'flaskd3',
    'host_ip': 'mysql',
    'db_name': 'flaskd3'
}


########
# util #
########
def _create_mysql_client():
    return MySQLClient(
        valid_param['user_name'],
        valid_param['password'],
        valid_param['host_ip'],
        valid_param['db_name']
    )


def _extract_only_column_name(table_name, columns):
    column_names = []
    delete_initial_chars = len(table_name) + 1  # table_name.***
    for column in columns:
        column_names.append(str(column)[delete_initial_chars:])
    column_names.sort()
    return column_names


########
# test #
########
def test_mysql_client_init():
    client = _create_mysql_client()
    expect_url = 'mysql+mysqldb://flaskd3:flaskd3@mysql/flaskd3?charset=utf8'
    assert client.url == expect_url
    assert isinstance(client.Session, scoped_session)


def test_create_models():
    client = _create_mysql_client()
    client.create_models()
    # SHOW TABLES
    keys = client.base.metadata.tables.keys()
    sorted_keys = sorted(keys)
    expect_tables = ['data_types', 'regions', 'data', 'buckets', 'objects']
    expect_tables.sort()
    assert sorted_keys == expect_tables
    # DESC each TABLES
    expect_columns = []
    for table_name, table in client.base.metadata.tables.items():
        print(f'{table_name}:', table.columns)
        print('_extract_only_column_name:', _extract_only_column_name(table_name, table.columns))
        if table_name == 'data_types':
            expect_columns = ['name']
        if table_name == 'regions':
            expect_columns = ['name']
        if table_name == 'data':
            expect_columns = [
                'id',
                'user_id',
                'name',
                'data_type',
                'created_at',
                'updated_at',
                'deleted_at'
            ]
            expect_columns.sort()
        if table_name == 'buckets':
            expect_columns = [
                'id',
                'user_id',
                'name',
                'region',
                'created_at',
                'updated_at',
                'deleted_at'
            ]
            expect_columns.sort()
        if table_name == 'objects':
            expect_columns = [
                'id',
                'user_id',
                'name',
                'region',
                'version',
                'data_id',
                'bucket_id',
                'created_at',
                'updated_at',
                'deleted_at'
            ]
            expect_columns.sort()
        actual_columns = _extract_only_column_name(table_name, table.columns)
        assert actual_columns == expect_columns
