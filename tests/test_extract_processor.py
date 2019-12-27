import os
from src.extract_processor import extract_processor
from tests import *
import unittest
from unittest.mock import Mock, patch
import requests
import responses
import pytest
import boto3
from moto import mock_s3
from datetime import datetime, timezone
import tempfile
import csv

messageMissingConfig = "Lambda function not properly configured. Missing environment variable '{0:s}'."

@mock_s3
class ExtractProcessorTests(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def reset_env(self):
        os.environ.clear()

    def test_configerror_bucketname(self):
        os.environ["S3_BUCKET"] = ""

        # Compose the event body
        body = None
        file_path = os.path.join(os.path.dirname(__file__),"data/account_extract.json")
        with open(file_path, "r") as outfile:
            reqObj = json.load(outfile)
            body = reqObj

        # Invoke the handler
        resp = extract_processor.handler(api_gateway_event(body), None)

        # Verify assertions
        assert resp == { 'statusCode': 500, 'body': json.dumps(messageMissingConfig.format("S3_BUCKET")) }

    def test_configerror_s3fileformat(self):
        os.environ["S3_BUCKET"] = "hull-se-test"
        os.environ["S3_FILE_FORMAT"] = "foo"

        # Compose the event body
        body = None
        file_path = os.path.join(os.path.dirname(__file__),"data/account_extract.json")
        with open(file_path, "r") as outfile:
            reqObj = json.load(outfile)
            body = reqObj

        # Invoke the handler
        resp = extract_processor.handler(api_gateway_event(body), None)

        # Verify assertions
        error_msg = "Lambda function not properly configured. File format '{0:s}' is not one of the allowed values of 'csv' or 'json'."
        assert resp == { 'statusCode': 500, 'body': json.dumps(error_msg.format("foo")) }

    def test_invalidrequestbody(self):
        os.environ["S3_BUCKET"] = "hull-se-test"

        # Compose the event body
        body = { "foo": "bar" }
        
        # Invoke the handler
        resp = extract_processor.handler(api_gateway_event(body), None)

        # Verify assertions
        assert resp == { 'statusCode': 200, 'body': json.dumps("Nothing to process.") }

    @responses.activate
    def test_extract_is_successful(self):
        # Configure the mock to fake the get request
        download_content_path = os.path.join(os.path.dirname(__file__),"data/account_extract_download.json")
        with open(download_content_path, 'r') as download_file:
            res_body = download_file.read()
            responses.add(responses.GET, "https://somewhereinthecloud.local.host/extracts/account_report/test.json", body=res_body)
        
        # Now let's fake S3 using moto
        conn = boto3.resource('s3', region_name='us-east-1')
        s3clnt = boto3.client('s3', region_name='us-east-1')
        # pylint: disable=no-member
        conn.create_bucket(Bucket="hull-se-test")
        
        # Minimum env config
        os.environ["S3_BUCKET"] = "hull-se-test"

        # Compose the event body
        body = None
        file_path = os.path.join(os.path.dirname(__file__),"data/account_extract.json")
        with open(file_path, "r") as outfile:
            reqObj = json.load(outfile)
            body = reqObj

        # Invoke the handler
        resp = extract_processor.handler(api_gateway_event(body), None)

        # Verify assertions
        assert None != s3clnt.get_object(Bucket="hull-se-test", Key="account_extract_5e032e118ee92e9586007425.csv")
        assert resp == {
            'statusCode': 200,
            'body': json.dumps("Successfully processed extract.")
        }

    @responses.activate
    def test_singlefile_is_successful(self):
        # Configure the mock to fake the get request
        download_content_path = os.path.join(os.path.dirname(__file__),"data/account_extract_download.json")
        with open(download_content_path, 'r') as download_file:
            res_body = download_file.read()
            responses.add(responses.GET, "https://somewhereinthecloud.local.host/extracts/account_report/test.json", body=res_body)
        
        # Now let's fake S3 using moto
        conn = boto3.resource('s3', region_name='us-east-1')
        s3clnt = boto3.client('s3', region_name='us-east-1')
        # pylint: disable=no-member
        conn.create_bucket(Bucket="hull-se-test")
        
        # Extended env config
        os.environ["S3_BUCKET"] = "hull-se-test"
        os.environ["S3_SINGLEFILE"] = "my-single-file"

        # Compose the event body
        body = None
        file_path = os.path.join(os.path.dirname(__file__),"data/account_extract.json")
        with open(file_path, "r") as outfile:
            reqObj = json.load(outfile)
            body = reqObj

        # Invoke the handler
        resp = extract_processor.handler(api_gateway_event(body), None)

        # Verify assertions
        assert None != s3clnt.get_object(Bucket="hull-se-test", Key="my-single-file.csv")
        assert resp == {
            'statusCode': 200,
            'body': json.dumps("Successfully processed extract.")
        }

    @responses.activate
    def test_dayfolder_is_successful(self):
        # Configure the mock to fake the get request
        download_content_path = os.path.join(os.path.dirname(__file__),"data/account_extract_download.json")
        with open(download_content_path, 'r') as download_file:
            res_body = download_file.read()
            responses.add(responses.GET, "https://somewhereinthecloud.local.host/extracts/account_report/test.json", body=res_body)
        
        # Now let's fake S3 using moto
        conn = boto3.resource('s3', region_name='us-east-1')
        s3clnt = boto3.client('s3', region_name='us-east-1')
        # pylint: disable=no-member
        conn.create_bucket(Bucket="hull-se-test")
        
        # Extended env config
        os.environ["S3_BUCKET"] = "hull-se-test"
        os.environ["S3_DAILYFOLDER"] = "True"

        # Compose the event body
        body = None
        file_path = os.path.join(os.path.dirname(__file__),"data/account_extract.json")
        with open(file_path, "r") as outfile:
            reqObj = json.load(outfile)
            body = reqObj

        # Invoke the handler
        resp = extract_processor.handler(api_gateway_event(body), None)

        # Verify assertions
        now = datetime.now(tz=timezone.utc)
        assert None != s3clnt.get_object(Bucket="hull-se-test", Key=f"{now:%Y-%m-%d}/account_extract_5e032e118ee92e9586007425.csv")
        assert resp == {
            'statusCode': 200,
            'body': json.dumps("Successfully processed extract.")
        }

    @responses.activate
    def test_dailysinglefile_is_successful(self):
        # Configure the mock to fake the get request
        download_content_path = os.path.join(os.path.dirname(__file__),"data/account_extract_download.json")
        with open(download_content_path, 'r') as download_file:
            res_body = download_file.read()
            responses.add(responses.GET, "https://somewhereinthecloud.local.host/extracts/account_report/test.json", body=res_body)
        
        # Now let's fake S3 using moto
        conn = boto3.resource('s3', region_name='us-east-1')
        s3clnt = boto3.client('s3', region_name='us-east-1')
        # pylint: disable=no-member
        conn.create_bucket(Bucket="hull-se-test")
        
        # Extended env config
        os.environ["S3_BUCKET"] = "hull-se-test"
        os.environ["S3_DAILYFOLDER"] = "True"
        os.environ["S3_SINGLEFILE"] = "my-daily-file"

        # Compose the event body
        body = None
        file_path = os.path.join(os.path.dirname(__file__),"data/account_extract.json")
        with open(file_path, "r") as outfile:
            reqObj = json.load(outfile)
            body = reqObj

        # Invoke the handler
        resp = extract_processor.handler(api_gateway_event(body), None)

        # Verify assertions
        now = datetime.now(tz=timezone.utc)
        assert None != s3clnt.get_object(Bucket="hull-se-test", Key=f"{now:%Y-%m-%d}/my-daily-file.csv")
        assert resp == {
            'statusCode': 200,
            'body': json.dumps("Successfully processed extract.")
        }

    @responses.activate
    def test_singlefilewithfalsedaily_is_successful(self):
        # Configure the mock to fake the get request
        download_content_path = os.path.join(os.path.dirname(__file__),"data/account_extract_download.json")
        with open(download_content_path, 'r') as download_file:
            res_body = download_file.read()
            responses.add(responses.GET, "https://somewhereinthecloud.local.host/extracts/account_report/test.json", body=res_body)
        
        # Now let's fake S3 using moto
        conn = boto3.resource('s3', region_name='us-east-1')
        s3clnt = boto3.client('s3', region_name='us-east-1')
        # pylint: disable=no-member
        conn.create_bucket(Bucket="hull-se-test")
        
        # Extended env config
        os.environ["S3_BUCKET"] = "hull-se-test"
        os.environ["S3_DAILYFOLDER"] = "False"
        os.environ["S3_SINGLEFILE"] = "my-single-file2"

        # Compose the event body
        body = None
        file_path = os.path.join(os.path.dirname(__file__),"data/account_extract.json")
        with open(file_path, "r") as outfile:
            reqObj = json.load(outfile)
            body = reqObj

        # Invoke the handler
        resp = extract_processor.handler(api_gateway_event(body), None)

        # Verify assertions
        assert None != s3clnt.get_object(Bucket="hull-se-test", Key="my-single-file2.csv")
        assert resp == {
            'statusCode': 200,
            'body': json.dumps("Successfully processed extract.")
        }

    @responses.activate
    def test_bucketdoesntexist_fails(self):
        # Configure the mock to fake the get request
        download_content_path = os.path.join(os.path.dirname(__file__),"data/account_extract_download.json")
        with open(download_content_path, 'r') as download_file:
            res_body = download_file.read()
            responses.add(responses.GET, "https://somewhereinthecloud.local.host/extracts/account_report/test.json", body=res_body)
        
        # Now let's fake S3 using moto
        conn = boto3.resource('s3', region_name='us-east-1')
        # pylint: disable=no-member
        conn.create_bucket(Bucket="hull-se-test")
        
        # Extended env config
        os.environ["S3_BUCKET"] = "foo"
        os.environ["S3_SINGLEFILE"] = "my-single-file"

        # Compose the event body
        body = None
        file_path = os.path.join(os.path.dirname(__file__),"data/account_extract.json")
        with open(file_path, "r") as outfile:
            reqObj = json.load(outfile)
            body = reqObj

        # Invoke the handler
        resp = extract_processor.handler(api_gateway_event(body), None)

        # Verify assertions
        assert resp['statusCode'] == 500

    @responses.activate
    def test_userextract_is_successful(self):
        # Configure the mock to fake the get request
        download_content_path = os.path.join(os.path.dirname(__file__),"data/user_extract_download.json")
        with open(download_content_path, 'r') as download_file:
            res_body = download_file.read()
            responses.reset()
            responses.add(responses.GET, "https://somewhereinthecloud.hull.net/extracts/user_report/test.json", body=res_body)
        
        # Now let's fake S3 using moto
        conn = boto3.resource('s3', region_name='us-east-1')
        s3clnt = boto3.client('s3', region_name='us-east-1')
        # pylint: disable=no-member
        conn.create_bucket(Bucket="hull-se-test")
        
        # Minimum env config
        os.environ["S3_BUCKET"] = "hull-se-test"
        os.environ["S3_SINGLEFILE"] = "my-userextract"
        os.environ['HULL_EXPORT_FIELDS'] = json.dumps(["id", "email", "name", "external_id", "segment_ids"])

        # Compose the event body
        body = None
        file_path = os.path.join(os.path.dirname(__file__),"data/user_extract.json")
        with open(file_path, "r") as outfile:
            reqObj = json.load(outfile)
            body = reqObj

        # Invoke the handler
        resp = extract_processor.handler(api_gateway_event(body), None)

        # Verify assertions
        assert None != s3clnt.get_object(Bucket="hull-se-test", Key="my-userextract.csv")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = os.path.join(tmpdir, "my-userextract.csv")
            s3clnt.download_file("hull-se-test", "my-userextract.csv", tmp_path)
            print(tmp_path)
            with open(tmp_path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                for i, line in enumerate(reader):
                    if i == 0:
                        assert line == ["id", "email", "name", "external_id", "segment_ids", "segment_names"]
            
            os.remove(tmp_path)
        
        assert resp == {
            'statusCode': 200,
            'body': json.dumps("Successfully processed extract.")
        }
