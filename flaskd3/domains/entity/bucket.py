from copy import copy
from datetime import datetime

from dateutil.tz import tzutc


class Bucket:
    def __init__(
            self,
            user_id,
            name,
            region,
            id=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            # TODO : define default delete time as const
            deleted_at=datetime(9999, 12, 31, 23, 59, 59, 0, tzinfo=tzutc())
    ):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.region = region
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    # copy is the method to copy Bucket instance
    def copy(self):
        # NOTE: should not use copy.deepcopy because it is very slow
        copied = copy(self)
        return copied
