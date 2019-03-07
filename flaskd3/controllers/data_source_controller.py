# DataSourceController is the interface of dataSourceController
class DataSourceController:

    # data_source_use_case_input_port_if is _DataSourceUseCaseInputPortIF interface
    def __init__(self, data_source_use_case_input_port_if):
        self.input_port = data_source_use_case_input_port_if

    def execute(self, req):  # req = dict{"string": "string"}
        self.input_port.handle(req)  # NOTE: hatobaAPIでは input_port.handle() = CreateClusterAPIUsecase.Executeと同意(createClusterAPIUsecaseではないよ)
