from .input_port import DataSourceUseCaseInputPort
from flaskd3.domains import *

# inherit DataSourceUseCaseInputPort interface
class CreateDataSourceUseCaseInteractor(DataSourceUseCaseInputPort):

    # constructor for CreateDataSourceUseCase
    def __init__(self, data_source_use_case_out_port):
        self.output_port = data_source_use_case_out_port

    # this method should be moved domain layer
    def _dict_to_data_source_model(self, dic):
        try:
            data_source = DataSource(
                dic["user_id"],
                dic["name"],

            )

        except Exception as e:
            return e


    # handle is the method to handle 'CreateDataSource' request
    def handle(self, req):
        # TODO: call validator to request
        try:
            self._dict_to_data_source_model(req)
            res = req
        # error should be handled on out put port layer
        except Exception as e:
            return e
        self.output_port.emit(res)
