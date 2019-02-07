from datetime import datetime

from dateutil.tz import tzutc


class Object:
    def __init__(
        self,
        user_id,
        name,
        region,
        id=None,
        version_id=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        # TODO : define default delete time as const
        deleted_at=datetime(9999, 12, 31, 23, 59, 59, 0, tzinfo=tzutc())
    ):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.region = region
        self._version_id = version_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    # Getter for version_id
    @property
    def version_id(self):
        return self._version_id

    # Setter for version_id
    @version_id.setter
    def version_id(self, version_id):
        self._version_id = version_id
