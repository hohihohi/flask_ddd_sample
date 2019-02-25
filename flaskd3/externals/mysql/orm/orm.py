from contextlib import contextmanager
from retry.api import retry_call
from sqlalchemy import *
from sqlalchemy.orm import *

from .tables import *

ENCODING = 'utf-8'


# 1. use Base=declarative_base()
# 2. connect RDBMS to call create_engine
# 3. create tables if tables are not found to call create_all
class MySQLClient(object):

    # set up engine and session
    def __init__(self, user_name, password, host_ip, db_name, echo=False, pool_recycle=600):
        self._url = MySQLClient._setup_url(user_name, password, host_ip, db_name)
        self.engine = create_engine(
            self._url,
            encoding=ENCODING,
            echo=echo,
            pool_recycle=pool_recycle
        )
        self.Session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
        )
        # TODO: use session.query_property()
        # table classes should be inherited on self.base
        self._base = Base

    @staticmethod
    def _setup_url(user_name, password, host_ip, db_name):
        return f'mysql+mysqldb://{user_name}:{password}@{host_ip}/{db_name}?charset=utf8'

    @property
    def url(self):
        return self._url

    @property
    def base(self):
        return self._base

    def create_models(self):
        self._base.metadata.create_all(bind=self.engine)

    @contextmanager
    def create_session(self):
        s = self.Session()
        try:
            # __enter__
            retry_call(s.execute, fargs=['SELECT 1'], tries=6, delay=10)
            yield s
        finally:
            # __exit__
            s.close()
