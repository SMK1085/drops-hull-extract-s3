import os
import json
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import logging

logger = logging.getLogger()

def __create_env_error_response(var_name: str):
    message = "Lambda function not properly configured. Missing environment variable '{0:s}'."
    logger.error(message.format(var_name))
    response = {
        'statusCode': 500,
        'body': json.dumps(message.format(var_name))
    }
    return response

def handler(event, context):
    # Load the environment variables
    load_dotenv()
    # Configure log level
    logger.setLevel(os.getenv("HULL_LOG_LEVEL", logging.ERROR))
    # Log invocation
    logger.info("Hull extract requester invoked with event: %s", event)

    # Parse the environment variables
    logger.info("Parsing configuration from environment variables")

    HULL_ORG = os.getenv("HULL_ORG_ID")
    CONNECTOR_ID = os.getenv("HULL_CONNECTOR_ID")
    CONNECTOR_SECRET = os.getenv("HULL_CONNECTOR_SECRET")
    CALLBACK_URL = os.getenv("HULL_EXPORT_CALLBACKURL")
    HULL_OBJECTTYPE = os.getenv("HULL_EXPORT_OBJECTTYPE")
    HULL_FIELDS = os.getenv("HULL_EXPORT_FIELDS")
    HULL_ESQUERY = os.getenv("HULL_EXPORT_ESQUERY")

    logger.info("Loaded environment variables: %s", { 
        "HULL_ORG_ID": HULL_ORG,
        "HULL_CONNECTOR_ID": CONNECTOR_ID,
        "HULL_CONNECTOR_SECRET": CONNECTOR_SECRET,
        "HULL_EXPORT_CALLBACKURL": CALLBACK_URL,
        "HULL_EXPORT_OBJECTTYPE": HULL_OBJECTTYPE,
        "HULL_EXPORT_FIELDS": HULL_FIELDS,
        "HULL_EXPORT_ESQUERY": HULL_ESQUERY
    })

    # Perform pre-flight checks
    if not HULL_ORG:
        return __create_env_error_response("HULL_ORG_ID")
    
    if not CONNECTOR_ID:
        return __create_env_error_response("HULL_CONNECTOR_ID")
    
    if not CONNECTOR_SECRET:
        return __create_env_error_response("HULL_CONNECTOR_SECRET")
    
    if not CALLBACK_URL:
        return __create_env_error_response("HULL_EXPORT_CALLBACKURL")

    if not HULL_OBJECTTYPE:
        return __create_env_error_response("HULL_EXPORT_OBJECTTYPE")
    
    if not HULL_FIELDS:
        return __create_env_error_response("HULL_EXPORT_FIELDS")

    if not HULL_ESQUERY:
        return __create_env_error_response("HULL_EXPORT_ESQUERY")

    if HULL_OBJECTTYPE not in ["user", "account"]:
        message = "Lambda function not properly configured. Object type '{0:s}' is not one of the allowed values of 'user' or 'account'."
        logger.error(message.format(HULL_OBJECTTYPE))
        response = {
            'statusCode': 500,
            'body': json.dumps(message.format(HULL_OBJECTTYPE))
        }
        return response

    # All pre-flight checks have passed, so we are ready to request the extract
    try:
        export_url = f"https://{HULL_ORG}/api/v1/extract/{HULL_OBJECTTYPE}s"
        req_body = {
            "url": CALLBACK_URL,
            "format": "json",
            "fields": json.loads(HULL_FIELDS),
            "query": json.loads(HULL_ESQUERY)
        }
        req_headers = {
            "Accept": "application/json",
            "Hull-App-Id": CONNECTOR_ID,
            "Hull-Access-Token": CONNECTOR_SECRET
        }
        logger.info("Requesting extract from the Hull platform at url '%s' with headers %s and body %s", export_url, req_headers, req_body)
        response = requests.post(export_url, json=req_body, headers=req_headers)
        logger.info("Extract requested, finished with status: %s %s", response.status_code, response.reason)
        response.raise_for_status()

    except HTTPError as http_error:
        logger.error("An unexpected HTTP error occurred: %s", http_error)
        response = {
            'statusCode': http_error.response.status_code,
            'body': json.dumps(f"An unexpected HTTP error occurred: {http_error}")
        }
        return response
    except Exception as err:
        logger.error("An unexpected error occurred: %s", err)
        response = {
            'statusCode': 500,
            'body': json.dumps(f"An unexpected error occurred: {err}")
        }
        return response
    else:
        logger.info("Successully requested export from Hull. Result will be sent to '%s'", CALLBACK_URL)
        response = {
            'statusCode': 200,
            'body': json.dumps(f"Successully requested export from Hull. Result will be sent to '{CALLBACK_URL}'")
        }
        return response
