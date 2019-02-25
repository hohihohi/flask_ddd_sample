from copy import copy
from datetime import datetime

from dateutil.tz import tzutc


class Object:
    def __init__(
        self,
        user_id,
        name,
        region,
        id=None,
        version='unknown',
        bucket=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        # TODO : define default delete time as const
        deleted_at=datetime(9999, 12, 31, 23, 59, 59, 0, tzinfo=tzutc())
    ):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.region = region
        self._version = version
        self._bucket = bucket
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    # Getter for bucket
    @property
    def bucket(self):
        return self._bucket

    # Getter for version_id
    @property
    def version(self):
        return self._version

    # Setter for version_id
    @version.setter
    def version(self, version):
        self._version = version

    # copy is the method to copy Object instance
    def copy(self):
        return copy(self)
