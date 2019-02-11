from abc import ABCMeta, abstractmethod


# RestAPIOutputPort is the out port for the API which contains DataSource etc...
class RestAPIOutputPort(metaclass=ABCMeta):
    # emit is the method to emit each api
    @abstractmethod
    def emit(self, data):  # data is the output source. It is nearly response data and may be string[]
        pass
