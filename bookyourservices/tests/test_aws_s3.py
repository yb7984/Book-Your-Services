from unittest import TestCase
from aws.aws_s3 import *
from config import STATIC_FOLDER
import os;

class AWSS3Test(TestCase):
    """Test class for AWS S3"""
    @classmethod
    def setUpClass(cls):
        """Setup before test"""

    @classmethod
    def tearDownClass(cls):
        """Run after test"""

    def setUp(self):
        """Before the test."""

    def tearDown(self):
        """Clean up test data"""

    def test_upload_file(self):
        """test upload_file"""


        AWSS3Handler.upload_file(
            os.path.join(STATIC_FOLDER , "images/default-service.jpg") , 
            "bookyourservices" ,
            "images/bg.jpg")



