from abc import ABCMeta, abstractmethod


class BucketDomainServiceIF(metaclass=ABCMeta):
    # create bucket through call external object storage API method
    @abstractmethod
    def create_bucket(self, bucket_id):
        pass

    # update bucket through call external object storage API method
    @abstractmethod
    def update_bucket(self, bucket_id, new_bucket):
        pass

    # delete bucket through call external object storage API method
    @abstractmethod
    def delete_bucket(self, bucket_id):
        pass

    # describe bucket through call external object storage API method
    @abstractmethod
    def describe_buckets(self, user, name=""):
        pass
