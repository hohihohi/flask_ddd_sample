from abc import ABCMeta, abstractmethod


# NOTE: domain service concern with domain and business logic, so call them and has responsibility.
class ObjectRepositoryIF(metaclass=ABCMeta):
    # find object source by id from database. This method should return object or None
    @abstractmethod
    def find_by_id(self, id):
        pass

    # find object source by name from database. This method should return object or None
    @abstractmethod
    def find_by_name(self, name):
        pass

    # find object sources by user id from database. This method should return object or None
    @abstractmethod
    def find_by_user_id(self, user_id):
        pass

    # save object source to database. This method should return saved object or error
    @abstractmethod
    def save(self, data_source):
        pass

    # save bucket source database. This method should return saved bucket or error
    @abstractmethod
    def save_bucket(self, data_source):
        pass

    # delete object source from database. This method should return deleted object or error
    @abstractmethod
    def delete(self, data_source):
        pass

    # delete bucket source from database. This method should return deleted bucket or error
    @abstractmethod
    def delete_bucket(self, data_source):
        pass

    # update object source to database. This method should return updated object or error
    @abstractmethod
    def update(self, data_source):
        pass
