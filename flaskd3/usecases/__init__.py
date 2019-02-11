# Use-case layer responsibility
# 1. define UseCaseInteractor class which inherits inputPort interface
# And UseCaseInteractor has handle method and return outputPort, so it depends on Outputport interface
# 2. define inputPort interface which has handle method and it should depends on some domain services


from flaskd3.usecases.datasources import CreateDataSourceUseCaseInteractor, DataSourceUseCaseInputPort
