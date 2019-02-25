from .output_port import RestAPIOutputPort


class JSONPresenter(RestAPIOutputPort):
    def __init__(self):
        super()

    def emit(self, data):
        # usecase層でのレスポンスをユーザに返すための層: 本クラスはAPIレスポンスとしてユーザに返すための層
        # Console.WriteLine(data)
        pass

    def convert_internal_err_to_customer_err(self, err):
        pass
