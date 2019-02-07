from .data_source import DataSource, DataType
from .object import Object


def main():
    data_source = DataSource("xxx12345", "test", "RAW", "west")
    print(f"data_source.{data_source.__dict__}")


if __name__ == '__main__':
    main()
