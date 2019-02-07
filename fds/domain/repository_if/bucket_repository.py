from abc import ABCMeta, abstractmethod


# NOTE: domain service concern with domain and business logic, so call them and has responsibility.
class BucketRepositoryIF(metaclass=ABCMeta):
    # find data source by id from database. This method should return data source object or None
    @abstractmethod
    def find_by_id(self, id):
        pass

    # find data source by name from database. This method should return data source object or None
    @abstractmethod
    def find_by_name(self, name):
        pass

    # find data sources by user id from database. This method should return data sources object or None
    @abstractmethod
    def find_by_user_id(self, user_id):
        pass

    # save data source with the object to database. This method should return saved data source object or error
    @abstractmethod
    def save(self, data_source):
        pass

    # delete data source with the object from database. This method should return deleted data source object or error
    @abstractmethod
    def delete(self, data_source):
        pass

    # update data source with the object to database. This method should return updated data source object or error
    @abstractmethod
    def update(self, data_source):
        pass
