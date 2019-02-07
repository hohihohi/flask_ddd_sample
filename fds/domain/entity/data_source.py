from copy import copy
from datetime import datetime
from enum import Enum, auto

from dateutil.tz import tzutc

from .object import Object


class DataType(Enum):
    RAW = auto()
    PRE_PROCESSED = auto()
    PREDICTED = auto()

    @classmethod
    def describe(cls):
        # cls.name in the members
        ls = []
        for data_type in cls:
            ls.append(data_type.name)
        return ls


class DataSource:

    def __init__(
            self,
            user_id,
            name,
            data_type,
            region,
            id=None,
            df=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            # TODO : define default delete time as const
            deleted_at=datetime(9999, 12, 31, 23, 59, 59, 0, tzinfo=tzutc())
    ):
        self.id = id
        self.user_id = user_id
        self.name = name
        # TODO: check df is pandas.dataframe object or None
        self._df = df
        self._object = Object(user_id, name, region)
        if data_type not in DataType.describe():
            raise Exception("invalid data source type")
        self.data_type = DataType[data_type]
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    # Getter for object
    @property
    def object(self):
        return self._object

    # Setter for object
    @object.setter
    def object(self, object):
        self._object = object

    # copy is the method to copy DataType instance
    def copy(self):
        # NOTE: should not use copy.deepcopy because it is very slow
        copied = copy(self)
        copied.object = self._object.copy()
        return copied
