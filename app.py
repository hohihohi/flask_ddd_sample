# from flask import Flask, make_response, jsonify
from flask import Flask
# import base64

from .flaskd3.domains import DataSource
from .flaskd3.presenters import DataSourceUseCaseOutputPort


# MIME_CSV = "text/csv"
app = Flask(__name__)


@app.route("/")
def hello():
    data_source = DataSource("xxx12345", "test", "RAW", "west")
    print(f"data_source:{data_source.__dict__}")
    copied = data_source.copy()
    print(f"copied:{copied.__dict__}")
    print(f"data_source.obj:{data_source.object.__dict__}")
    print(f"data_source.obj:{copied.object.__dict__}")
    return "Hello, Flask!"


def main_program():
    # router層を作成し、routerでどのcontrollerを呼び出すか制御するとうまく行きそう
    # application 立ち上げ: command -> di(output->interactor->controller生成 -> router,workerに注入)
    # routerの挙動
    # 1. http request
    # 2. router.routing
    # 3. handle controller -> controller.execute
    # 4. input_port.handle(=実態はusecase.handle)
    # 5. output_port.emit
    outputPort = CreateOutputPort() # define CreateOutputPort(di)
    interactor = CreateInputPort(outputPort)  # define CreateOutputPort(di)
    controller = Controller(interactor) # define
    controller.Execute({"source", "data", "foo", "bar"})

# @app.route('/download/json', methods=['GET'])
# def report4():
#     file_name = 'hoge.csv'
#     # TODO: should use with
#     file_data_as_binary = open(file_name, 'rb').read()
#
#     download_data = {
#         'fileName': file_name,
#         'contentType': MIME_CSV,
#         'contentData': base64.b64encode(file_data_as_binary) # encode to base64
#     }
#
#     return make_response(jsonify(download_data))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
