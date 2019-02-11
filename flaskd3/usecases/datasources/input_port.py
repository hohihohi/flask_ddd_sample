from abc import ABCMeta, abstractmethod


# DataSourceUseCaseInputPort is the input port for DataSource API
class DataSourceUseCaseInputPort(metaclass=ABCMeta):
    # handle is the method to handle each data source api
    @abstractmethod
    def handle(self, data):  # data is the input source. It is nearly request data and may be string[]
        pass
