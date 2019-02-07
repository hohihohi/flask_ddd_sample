from abc import ABCMeta, abstractmethod


class ObjectDomainServiceIF(metaclass=ABCMeta):
    # create object through call external object storage API method
    @abstractmethod
    def create_object(self, object_id):
        pass

    # update object through call external object storage API method
    @abstractmethod
    def update_object(self, object_id, new_object):
        pass

    # delete object through call external object storage API method
    @abstractmethod
    def delete_object(self, object_id):
        pass

    # describe bucket through call external object storage API method
    @abstractmethod
    def describe_objects(self, user, name=""):
        pass
