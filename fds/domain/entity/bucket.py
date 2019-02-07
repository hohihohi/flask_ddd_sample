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
            objects=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            # TODO : define default delete time as const
            deleted_at=datetime(9999, 12, 31, 23, 59, 59, 0, tzinfo=tzutc())
    ):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.region = region
        if objects is None:
            self._objects = []
        else:
            self._objects = objects
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    # Getter for version_id
    @property
    def objects(self):
        return self._objects

    # Setter for version_id
    @objects.setter
    def objects(self, objects):
        self._objects = objects

    # get_object_by_name is the function to get the object from Bucket.objects
    # by name
    def get_object_by_name(self, object_name):
        for obj in self._objects:
            if obj.name == object_name:
                return object
        return None

    # copy is the method to copy Bucket instance
    def copy(self):
        # NOTE: should not use copy.deepcopy because it is very slow
        copied = copy(self)
        objects = []
        for obj in self._objects:
            objects.append(obj)
        copied.objects = objects
        return copied
