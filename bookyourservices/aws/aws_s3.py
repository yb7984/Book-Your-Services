import boto3
from botocore.exceptions import ClientError


class AWSS3Handler:
    """Class including methods handling aws s3"""

    def upload_file(file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(
                file_name,
                bucket,
                object_name,
                ExtraArgs={'ACL': 'public-read'})
        except ClientError as e:
            print(e)
            return False
        return True


    @staticmethod
    def object_url(bucket , object_name):
        """Return the object_url on AWS S3"""

        return f"https://{bucket}.s3.amazonaws.com/{object_name}"
