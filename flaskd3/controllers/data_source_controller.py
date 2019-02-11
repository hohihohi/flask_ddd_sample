# DataSourceController is the interface of dataSourceController
class DataSourceController:

    # data_source_use_case_input_port_if is _DataSourceUseCaseInputPortIF interface
    def __init__(self, data_source_use_case_input_port_if):
        self.input_port = data_source_use_case_input_port_if

    def execute(self):
        self.input_port.handle()  # NOTE: hatobaAPIでは input_port.handle() = CreateClusterAPIUsecase.Executeと同意(createClusterAPIUsecaseではないよ)
