from .input_port import DataSourceUseCaseInputPort
from flaskd3.domains import *

# inherit DataSourceUseCaseInputPort interface
class CreateDataSourceUseCaseInteractor(DataSourceUseCaseInputPort):

    # constructor for CreateDataSourceUseCase
    def __init__(self, data_source_use_case_out_port):
        self.output_port = data_source_use_case_out_port

    # handle is the method to handle 'CreateDataSource' request
    def handle(self, req):
        # TODO: call validator to request
        try:
            # TODO: check whether specified data is loadable as data frame or not
            # TODO: create data object
            # TODO: create dataframe
            # TODO: check whether new bucket is necessary or not
            # TODO: create bucket
            # TODO: create data source
            data_source = DataSource(
                req['user_id'],
                req['name'],
            )
            # TODO: save bucket
            # TODO: save data object
            # TODO: save data source
            # TODO: respond data source object(output port has convert process)
            res = req
        # error should be handled on out put port layer
        except Exception as e:
            return e
        self.output_port.emit(res)
