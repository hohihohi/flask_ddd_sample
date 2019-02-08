from flask import Flask

from fds.domains import DataSource


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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
