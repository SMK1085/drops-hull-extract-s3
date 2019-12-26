import os
from src.extract_requester import extract_requester
from tests import *
import unittest
from unittest.mock import Mock, patch
import requests
import pytest

messageMissingConfig = "Lambda function not properly configured. Missing environment variable '{0:s}'."

class ExtractRequesterTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def reset_env(self):
        os.environ["HULL_CONNECTOR_ID"] = ""
        os.environ["HULL_CONNECTOR_SECRET"] = ""
        os.environ["HULL_ORG_ID"] = ""
        os.environ["HULL_EXPORT_CALLBACKURL"] = ""
        os.environ["HULL_EXPORT_OBJECTTYPE"] = ""
        os.environ["HULL_EXPORT_FIELDS"] = ""
        os.environ["HULL_EXPORT_ESQUERY"] = ""

    def test_configerror_connectorid(self):
        # No mock needed, since we are not calling the Hull API

        # Set up the environment variables to make the test pass
        os.environ["HULL_CONNECTOR_SECRET"] = "sjhg3y8y8wnhmlaug9htuhwyio5hst"
        os.environ["HULL_ORG_ID"] = "foo.hullapp.io"
        os.environ["HULL_EXPORT_CALLBACKURL"] = "https://demo.somedomain.com/callback"
        os.environ["HULL_EXPORT_OBJECTTYPE"] = "account"
        os.environ["HULL_EXPORT_FIELDS"] = json.dumps(["name","domain","created_at","subscription_status","sm_stage","vitally_first_paid_date","stripe_current_subscription_status","vitally_last_seen_timestamp","vitally_messages_sent_by_agents_last7d"])
        os.environ["HULL_EXPORT_ESQUERY"] = json.dumps({"constant_score":{"filter":{"bool":{"filter":[{"range":{"vitally_first_paid_date":{"gt":"now-100d"}}},{"term":{"stripe_current_subscription_status.raw":"paying"}},{"bool":{"must_not":{"bool":{"minimum_should_match":1,"should":[{"prefix":{"vitally_last_seen_timestamp":"xxx"}},{"prefix":{"vitally_last_seen_timestamp.exact":"xxx"}}]}}}},{"range":{"vitally_messages_sent_by_agents_last7d":{"gt":25}}}]}}}})

        # It's just a scheduler event, so nothing to pass as payload
        resp = extract_requester.handler(api_gateway_event({}), None)
        assert resp == { 'statusCode': 500, 'body': json.dumps(messageMissingConfig.format("HULL_CONNECTOR_ID")) }

    def test_configerror_connectorsecret(self):
        # No mock needed, since we are not calling the Hull API

        # Set up the environment variables to make the test pass
        os.environ["HULL_CONNECTOR_ID"] = "gu2hn4hum9ujwjpheohtjodj"
        os.environ["HULL_ORG_ID"] = "foo.hullapp.io"
        os.environ["HULL_EXPORT_CALLBACKURL"] = "https://demo.somedomain.com/callback"
        os.environ["HULL_EXPORT_OBJECTTYPE"] = "account"
        os.environ["HULL_EXPORT_FIELDS"] = json.dumps(["name","domain","created_at","subscription_status","sm_stage","vitally_first_paid_date","stripe_current_subscription_status","vitally_last_seen_timestamp","vitally_messages_sent_by_agents_last7d"])
        os.environ["HULL_EXPORT_ESQUERY"] = json.dumps({"constant_score":{"filter":{"bool":{"filter":[{"range":{"vitally_first_paid_date":{"gt":"now-100d"}}},{"term":{"stripe_current_subscription_status.raw":"paying"}},{"bool":{"must_not":{"bool":{"minimum_should_match":1,"should":[{"prefix":{"vitally_last_seen_timestamp":"xxx"}},{"prefix":{"vitally_last_seen_timestamp.exact":"xxx"}}]}}}},{"range":{"vitally_messages_sent_by_agents_last7d":{"gt":25}}}]}}}})

        # It's just a scheduler event, so nothing to pass as payload
        resp = extract_requester.handler(api_gateway_event({}), None)
        assert resp == { 'statusCode': 500, 'body': json.dumps(messageMissingConfig.format("HULL_CONNECTOR_SECRET")) }

    def test_configerror_orgid(self):
        # No mock needed, since we are not calling the Hull API

        # Set up the environment variables to make the test pass
        os.environ["HULL_CONNECTOR_ID"] = "gu2hn4hum9ujwjpheohtjodj"
        os.environ["HULL_CONNECTOR_SECRET"] = "sjhg3y8y8wnhmlaug9htuhwyio5hst"
        os.environ["HULL_EXPORT_CALLBACKURL"] = "https://demo.somedomain.com/callback"
        os.environ["HULL_EXPORT_OBJECTTYPE"] = "account"
        os.environ["HULL_EXPORT_FIELDS"] = json.dumps(["name","domain","created_at","subscription_status","sm_stage","vitally_first_paid_date","stripe_current_subscription_status","vitally_last_seen_timestamp","vitally_messages_sent_by_agents_last7d"])
        os.environ["HULL_EXPORT_ESQUERY"] = json.dumps({"constant_score":{"filter":{"bool":{"filter":[{"range":{"vitally_first_paid_date":{"gt":"now-100d"}}},{"term":{"stripe_current_subscription_status.raw":"paying"}},{"bool":{"must_not":{"bool":{"minimum_should_match":1,"should":[{"prefix":{"vitally_last_seen_timestamp":"xxx"}},{"prefix":{"vitally_last_seen_timestamp.exact":"xxx"}}]}}}},{"range":{"vitally_messages_sent_by_agents_last7d":{"gt":25}}}]}}}})

        # It's just a scheduler event, so nothing to pass as payload
        resp = extract_requester.handler(api_gateway_event({}), None)
        assert resp == { 'statusCode': 500, 'body': json.dumps(messageMissingConfig.format("HULL_ORG_ID")) }
    
    def test_configerror_callback(self):
        # No mock needed, since we are not calling the Hull API

        # Set up the environment variables to make the test pass
        os.environ["HULL_CONNECTOR_ID"] = "gu2hn4hum9ujwjpheohtjodj"
        os.environ["HULL_CONNECTOR_SECRET"] = "sjhg3y8y8wnhmlaug9htuhwyio5hst"
        os.environ["HULL_ORG_ID"] = "foo.hullapp.io"
        os.environ["HULL_EXPORT_OBJECTTYPE"] = "account"
        os.environ["HULL_EXPORT_FIELDS"] = json.dumps(["name","domain","created_at","subscription_status","sm_stage","vitally_first_paid_date","stripe_current_subscription_status","vitally_last_seen_timestamp","vitally_messages_sent_by_agents_last7d"])
        os.environ["HULL_EXPORT_ESQUERY"] = json.dumps({"constant_score":{"filter":{"bool":{"filter":[{"range":{"vitally_first_paid_date":{"gt":"now-100d"}}},{"term":{"stripe_current_subscription_status.raw":"paying"}},{"bool":{"must_not":{"bool":{"minimum_should_match":1,"should":[{"prefix":{"vitally_last_seen_timestamp":"xxx"}},{"prefix":{"vitally_last_seen_timestamp.exact":"xxx"}}]}}}},{"range":{"vitally_messages_sent_by_agents_last7d":{"gt":25}}}]}}}})

        # It's just a scheduler event, so nothing to pass as payload
        resp = extract_requester.handler(api_gateway_event({}), None)
        assert resp == { 'statusCode': 500, 'body': json.dumps(messageMissingConfig.format("HULL_EXPORT_CALLBACKURL")) }
    
    def test_configerror_objecttype(self):
        # No mock needed, since we are not calling the Hull API

        # Set up the environment variables to make the test pass
        os.environ["HULL_CONNECTOR_ID"] = "gu2hn4hum9ujwjpheohtjodj"
        os.environ["HULL_CONNECTOR_SECRET"] = "sjhg3y8y8wnhmlaug9htuhwyio5hst"
        os.environ["HULL_ORG_ID"] = "foo.hullapp.io"
        os.environ["HULL_EXPORT_CALLBACKURL"] = "https://demo.somedomain.com/callback"
        os.environ["HULL_EXPORT_FIELDS"] = json.dumps(["name","domain","created_at","subscription_status","sm_stage","vitally_first_paid_date","stripe_current_subscription_status","vitally_last_seen_timestamp","vitally_messages_sent_by_agents_last7d"])
        os.environ["HULL_EXPORT_ESQUERY"] = json.dumps({"constant_score":{"filter":{"bool":{"filter":[{"range":{"vitally_first_paid_date":{"gt":"now-100d"}}},{"term":{"stripe_current_subscription_status.raw":"paying"}},{"bool":{"must_not":{"bool":{"minimum_should_match":1,"should":[{"prefix":{"vitally_last_seen_timestamp":"xxx"}},{"prefix":{"vitally_last_seen_timestamp.exact":"xxx"}}]}}}},{"range":{"vitally_messages_sent_by_agents_last7d":{"gt":25}}}]}}}})

        # It's just a scheduler event, so nothing to pass as payload
        resp = extract_requester.handler(api_gateway_event({}), None)
        assert resp == { 'statusCode': 500, 'body': json.dumps(messageMissingConfig.format("HULL_EXPORT_OBJECTTYPE")) }
    
    def test_configerror_fields(self):
        # No mock needed, since we are not calling the Hull API

        # Set up the environment variables to make the test pass
        os.environ["HULL_CONNECTOR_ID"] = "gu2hn4hum9ujwjpheohtjodj"
        os.environ["HULL_CONNECTOR_SECRET"] = "sjhg3y8y8wnhmlaug9htuhwyio5hst"
        os.environ["HULL_ORG_ID"] = "foo.hullapp.io"
        os.environ["HULL_EXPORT_CALLBACKURL"] = "https://demo.somedomain.com/callback"
        os.environ["HULL_EXPORT_OBJECTTYPE"] = "account"
        os.environ["HULL_EXPORT_ESQUERY"] = json.dumps({"constant_score":{"filter":{"bool":{"filter":[{"range":{"vitally_first_paid_date":{"gt":"now-100d"}}},{"term":{"stripe_current_subscription_status.raw":"paying"}},{"bool":{"must_not":{"bool":{"minimum_should_match":1,"should":[{"prefix":{"vitally_last_seen_timestamp":"xxx"}},{"prefix":{"vitally_last_seen_timestamp.exact":"xxx"}}]}}}},{"range":{"vitally_messages_sent_by_agents_last7d":{"gt":25}}}]}}}})

        # It's just a scheduler event, so nothing to pass as payload
        resp = extract_requester.handler(api_gateway_event({}), None)
        assert resp == { 'statusCode': 500, 'body': json.dumps(messageMissingConfig.format("HULL_EXPORT_FIELDS")) }
    
    def test_configerror_esquery(self):
        # No mock needed, since we are not calling the Hull API

        # Set up the environment variables to make the test pass
        os.environ["HULL_CONNECTOR_ID"] = "gu2hn4hum9ujwjpheohtjodj"
        os.environ["HULL_CONNECTOR_SECRET"] = "sjhg3y8y8wnhmlaug9htuhwyio5hst"
        os.environ["HULL_ORG_ID"] = "foo.hullapp.io"
        os.environ["HULL_EXPORT_CALLBACKURL"] = "https://demo.somedomain.com/callback"
        os.environ["HULL_EXPORT_OBJECTTYPE"] = "account"
        os.environ["HULL_EXPORT_FIELDS"] = json.dumps(["name","domain","created_at","subscription_status","sm_stage","vitally_first_paid_date","stripe_current_subscription_status","vitally_last_seen_timestamp","vitally_messages_sent_by_agents_last7d"])

        # It's just a scheduler event, so nothing to pass as payload
        resp = extract_requester.handler(api_gateway_event({}), None)
        assert resp == { 'statusCode': 500, 'body': json.dumps(messageMissingConfig.format("HULL_EXPORT_ESQUERY")) }

    def test_configerror_invalidobjecttype(self):
        # Set up the environment variables to make the test pass
        os.environ["HULL_CONNECTOR_ID"] = "gu2hn4hum9ujwjpheohtjodj"
        os.environ["HULL_CONNECTOR_SECRET"] = "sjhg3y8y8wnhmlaug9htuhwyio5hst"
        os.environ["HULL_ORG_ID"] = "foo.hullapp.io"
        os.environ["HULL_EXPORT_CALLBACKURL"] = "https://demo.somedomain.com/callback"
        os.environ["HULL_EXPORT_OBJECTTYPE"] = "foo"
        os.environ["HULL_EXPORT_FIELDS"] = json.dumps(["name","domain","created_at","subscription_status","sm_stage","vitally_first_paid_date","stripe_current_subscription_status","vitally_last_seen_timestamp","vitally_messages_sent_by_agents_last7d"])
        os.environ["HULL_EXPORT_ESQUERY"] = json.dumps({"constant_score":{"filter":{"bool":{"filter":[{"range":{"vitally_first_paid_date":{"gt":"now-100d"}}},{"term":{"stripe_current_subscription_status.raw":"paying"}},{"bool":{"must_not":{"bool":{"minimum_should_match":1,"should":[{"prefix":{"vitally_last_seen_timestamp":"xxx"}},{"prefix":{"vitally_last_seen_timestamp.exact":"xxx"}}]}}}},{"range":{"vitally_messages_sent_by_agents_last7d":{"gt":25}}}]}}}})

        msg = "Lambda function not properly configured. Object type 'foo' is not one of the allowed values of 'user' or 'account'."
        resp = extract_requester.handler(api_gateway_event({}), None)
        assert resp == { 'statusCode': 500, 'body': json.dumps(msg) }

    @patch("src.extract_requester.extract_requester.requests.post")
    def test_htmlerror_is_reported(self, mock_post):
        # Configure the Mock, let's pretend we have a 503 service unavailable
        mock_resp = requests.models.Response()
        mock_resp.status_code = 503
        mock_post.return_value = mock_resp

        # Set up the environment variables to make the test pass
        os.environ["HULL_CONNECTOR_ID"] = "gu2hn4hum9ujwjpheohtjodj"
        os.environ["HULL_CONNECTOR_SECRET"] = "sjhg3y8y8wnhmlaug9htuhwyio5hst"
        os.environ["HULL_ORG_ID"] = "foo.hullapp.io"
        os.environ["HULL_EXPORT_CALLBACKURL"] = "https://demo.somedomain.com/callback"
        os.environ["HULL_EXPORT_OBJECTTYPE"] = "account"
        os.environ["HULL_EXPORT_FIELDS"] = json.dumps(["name","domain","created_at","subscription_status","sm_stage","vitally_first_paid_date","stripe_current_subscription_status","vitally_last_seen_timestamp","vitally_messages_sent_by_agents_last7d"])
        os.environ["HULL_EXPORT_ESQUERY"] = json.dumps({"constant_score":{"filter":{"bool":{"filter":[{"range":{"vitally_first_paid_date":{"gt":"now-100d"}}},{"term":{"stripe_current_subscription_status.raw":"paying"}},{"bool":{"must_not":{"bool":{"minimum_should_match":1,"should":[{"prefix":{"vitally_last_seen_timestamp":"xxx"}},{"prefix":{"vitally_last_seen_timestamp.exact":"xxx"}}]}}}},{"range":{"vitally_messages_sent_by_agents_last7d":{"gt":25}}}]}}}})

        # It's just a scheduler event, so nothing to pass as payload
        resp = extract_requester.handler(api_gateway_event({}), None)
        assert resp == { 'statusCode': 503, 'body': json.dumps("An unexpected HTTP error occurred: 503 Server Error: None for url: None") }

    @patch("src.extract_requester.extract_requester.requests.post")
    def test_exception_is_reported(self, mock_post):
        # Configure the Mock
        mock_resp = requests.models.Response()
        mock_resp.status_code = 200
        mock_resp.json = {
            "url": "https://demo.somedomain.com/callback",
            "format": "json",
            "message": "Extract started. We'll send it to 'https://demo.somedomain.com/callback'"
        }
        mock_post.return_value = mock_resp

        # Set up the environment variables to make the test pass
        os.environ["HULL_CONNECTOR_ID"] = "gu2hn4hum9ujwjpheohtjodj"
        os.environ["HULL_CONNECTOR_SECRET"] = "sjhg3y8y8wnhmlaug9htuhwyio5hst"
        os.environ["HULL_ORG_ID"] = "foo.hullapp.io"
        os.environ["HULL_EXPORT_CALLBACKURL"] = "https://demo.somedomain.com/callback"
        os.environ["HULL_EXPORT_OBJECTTYPE"] = "account"
        os.environ["HULL_EXPORT_FIELDS"] = "some major foo"
        os.environ["HULL_EXPORT_ESQUERY"] = json.dumps({"constant_score":{"filter":{"bool":{"filter":[{"range":{"vitally_first_paid_date":{"gt":"now-100d"}}},{"term":{"stripe_current_subscription_status.raw":"paying"}},{"bool":{"must_not":{"bool":{"minimum_should_match":1,"should":[{"prefix":{"vitally_last_seen_timestamp":"xxx"}},{"prefix":{"vitally_last_seen_timestamp.exact":"xxx"}}]}}}},{"range":{"vitally_messages_sent_by_agents_last7d":{"gt":25}}}]}}}})

        # It's just a scheduler event, so nothing to pass as payload
        resp = extract_requester.handler(api_gateway_event({}), None)
        assert resp == { 'statusCode': 500, 'body': json.dumps("An unexpected error occurred: Expecting value: line 1 column 1 (char 0)")}



    @patch("src.extract_requester.extract_requester.requests.post")
    def test_export_is_successful(self, mock_post):
        # Configure the Mock
        mock_resp = requests.models.Response()
        mock_resp.status_code = 200
        mock_resp.json = {
            "url": "https://demo.somedomain.com/callback",
            "format": "json",
            "message": "Extract started. We'll send it to 'https://demo.somedomain.com/callback'"
        }
        mock_post.return_value = mock_resp

        # Set up the environment variables to make the test pass
        os.environ["HULL_CONNECTOR_ID"] = "gu2hn4hum9ujwjpheohtjodj"
        os.environ["HULL_CONNECTOR_SECRET"] = "sjhg3y8y8wnhmlaug9htuhwyio5hst"
        os.environ["HULL_ORG_ID"] = "foo.hullapp.io"
        os.environ["HULL_EXPORT_CALLBACKURL"] = "https://demo.somedomain.com/callback"
        os.environ["HULL_EXPORT_OBJECTTYPE"] = "account"
        os.environ["HULL_EXPORT_FIELDS"] = json.dumps(["name","domain","created_at","subscription_status","sm_stage","vitally_first_paid_date","stripe_current_subscription_status","vitally_last_seen_timestamp","vitally_messages_sent_by_agents_last7d"])
        os.environ["HULL_EXPORT_ESQUERY"] = json.dumps({"constant_score":{"filter":{"bool":{"filter":[{"range":{"vitally_first_paid_date":{"gt":"now-100d"}}},{"term":{"stripe_current_subscription_status.raw":"paying"}},{"bool":{"must_not":{"bool":{"minimum_should_match":1,"should":[{"prefix":{"vitally_last_seen_timestamp":"xxx"}},{"prefix":{"vitally_last_seen_timestamp.exact":"xxx"}}]}}}},{"range":{"vitally_messages_sent_by_agents_last7d":{"gt":25}}}]}}}})

        # It's just a scheduler event, so nothing to pass as payload
        resp = extract_requester.handler(api_gateway_event({}), None)
        assert resp == { 'statusCode': 200, 'body': json.dumps("Successully requested export from Hull. Result will be sent to 'https://demo.somedomain.com/callback'")}


if __name__ == "__main__":
    unittest.main()