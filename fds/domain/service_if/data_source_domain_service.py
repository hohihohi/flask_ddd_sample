from abc import ABCMeta, abstractmethod


# NOTE: domain service concern with domain logic, so call it and has responsibility.
class DataSourceDomainServiceIF(metaclass=ABCMeta):
    # update data source(df, object, name, type)
    @abstractmethod
    def update_data_source(self, data_source_id, new_name, new_df, new_object, new_type):
        pass
