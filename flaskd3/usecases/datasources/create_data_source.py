from .input_port import DataSourceUseCaseInputPort


# inherit DataSourceUseCaseInputPort interface
class CreateDataSourceUseCaseInteractor(DataSourceUseCaseInputPort):

    # constructor for CreateDataSourceUseCase
    def __init__(self, data_source_use_case_out_port):
        self.output_port = data_source_use_case_out_port

    # handle is the method to handle 'CreateDataSource' request
    def handle(self, data):
        res = data
        self.output_port.emit(res)
