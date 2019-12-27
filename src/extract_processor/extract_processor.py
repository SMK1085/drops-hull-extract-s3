import os
import json
import csv
import requests
import boto3
import botocore
from botocore.exceptions import ClientError
from datetime import datetime, timezone
import uuid
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

def __compose_segment_names(segments, segment_ids):
    seg_names = []
    for sid in segment_ids:
        segment = next(seg for seg in segments if seg['id'] == sid)
        if segment:
            seg_names.append(segment['name'])
    return seg_names

def handler(event, context):
    # Load the environment variables
    load_dotenv()
    # Configure log level
    logger.setLevel(os.getenv("HULL_LOG_LEVEL", logging.ERROR))
    # Log invocation
    logger.info("Hull extract processor invoked with event: %s", event)
    # Parse the environment variables
    logger.info("Parsing configuration from environment variables...")

    S3_BUCKET = os.getenv("S3_BUCKET") # The name of the S3 bucket
    S3_SINGLEFILE = os.getenv("S3_SINGLEFILE") # Used to have only one file
    S3_DAILYFOLDER = os.getenv("S3_DAILYFOLDER") # Used to create daily folders (UTC timezone)
    S3_FILE_FORMAT = os.getenv("S3_FILE_FORMAT", "csv") # Defines the file format; either csv or json
    HULL_FIELDS = os.getenv("HULL_EXPORT_FIELDS") # Used to overwrite auto-detection (recommended)

    logger.info("Loaded environment variables: %s", {
        "S3_BUCKET": S3_BUCKET,
        "S3_SINGLEFILE": S3_SINGLEFILE,
        "S3_DAILYFOLDER": S3_DAILYFOLDER,
        "S3_FILE_FORMAT": S3_FILE_FORMAT,
        "HULL_EXPORT_FIELDS": HULL_FIELDS
    })

    # Parse the body
    logger.info("Parsing request body from event...")
    body = json.loads(event['body'])
    file_url = body.get('url')
    notification_id = body.get('notification_id', f"{uuid.uuid4()}")
    notification_id_safe = notification_id.replace(":", "_")
    safe_name = f"{uuid.uuid4()}"
    object_type = body.get('object_type')
    account_segments = body.get('account_segments', "[]")
    user_segments = body.get('segments', "[]")

    logger.info("Parsed extract parameters: %s", {
        "file_url": file_url,
        "notification_id": notification_id,
        "object_type": object_type,
        "account_segments": account_segments,
        "user_segments": user_segments
    })

    # Perform pre-flight checks
    if not S3_BUCKET:
        return __create_env_error_response("S3_BUCKET")
    
    if S3_FILE_FORMAT not in ["csv", "json"]:
        message = "Lambda function not properly configured. File format '{0:s}' is not one of the allowed values of 'csv' or 'json'."
        logger.error(message.format(S3_FILE_FORMAT))
        response = {
            'statusCode': 500,
            'body': json.dumps(message.format(S3_FILE_FORMAT))
        }
        return response
    
    if not file_url:
        logger.warn("No file_url present in request body. Aborting processing...")
        response = {
            'statusCode': 200,
            'body': json.dumps("Nothing to process.")
        }
        return response

    # All pre-flight checks have passed, so we are ready to process the extract
    logger.info("Using temporary file for %s writer: /tmp/%s.%s", S3_FILE_FORMAT.upper(), safe_name, S3_FILE_FORMAT)
    tmp_file = open(f'/tmp/{safe_name}.{S3_FILE_FORMAT}', 'w')
    if S3_FILE_FORMAT == "json":
        json_data = []
        # Download the file
        logger.info("Requesting file from '%s'...", file_url)
        with requests.get(file_url, stream=True) as r:
            logger.info("Received file with status: %s %s", r.status_code, r.reason)
            r.raise_for_status()
            logger.info("Iterating over lines in file...")
            for line in r.iter_lines():
                if line:
                    logger.info("Received new line. Processing...")
                    decoded_line = line.decode("utf-8")
                    logger.info("Decoded line with utf-8: %s", decoded_line)
                    hull_obj = json.loads(decoded_line)
                    logger.info("Loaded JSON object.")
                    json_data.append(hull_obj)
            
            json.dump(json_data, tmp_file)
    else:
        csvwriter = csv.writer(tmp_file)
        row_count = 0
        header = None
        # Download the file
        logger.info("Requesting file from '%s'...", file_url)
        with requests.get(file_url, stream=True) as r:
            logger.info("Received file with status: %s %s", r.status_code, r.reason)
            r.raise_for_status()
            logger.info("Iterating over lines in file...")
            for line in r.iter_lines():
                if line:
                    logger.info("Received new line. Processing...")
                decoded_line = line.decode("utf-8")
                logger.info("Decoded line with utf-8: %s", decoded_line)
                hull_obj = json.loads(decoded_line)
                logger.info("Loaded JSON object.")
                if row_count == 0:
                    if HULL_FIELDS: 
                        logger.info("Using HULL_FIELDS from environment variables as CSV header.")
                        header = json.loads(HULL_FIELDS)
                    else:
                        logger.info("Detecting CSV header from first line...")
                        list_headers = []
                        for h in hull_obj.keys():
                            list_headers.append(h)
                        logger.info("Using the following header fields: %s", list_headers)
                        header = list_headers
                    
                    # add segment_names if segment_ids is present
                    if "segment_ids" in header:
                        logger.info("Adding segment_names to header since segment_ids is present...")
                        header.append("segment_names")
                        if object_type == "account_report":
                            hull_obj["segment_names"] = __compose_segment_names(account_segments, hull_obj["segment_ids"])
                        elif object_type == "user_report":
                            hull_obj["segment_names"] = __compose_segment_names(user_segments, hull_obj["segment_ids"])

                    csvwriter.writerow(header)
                    row_count += 1

                csv_obj = {}
                for key in header:
                    if key in hull_obj:
                        # The key is in the hull object specified, so just add the value
                        logger.info("Writing field %s with value %s", key, hull_obj[key])
                        csv_obj[key] = hull_obj[key]
                    elif key == "segment_names":
                        # Resolve the segment identifiers to human-readable names
                        if object_type == "account_report":
                            logger.info("Writing segment_names based on account segments with ids %s", hull_obj["segment_ids"])
                            csv_obj["segment_names"] = __compose_segment_names(account_segments, hull_obj["segment_ids"])
                        elif object_type == "user_report":
                            logger.info("Writing segment_names based on user segments with ids %s", hull_obj["segment_ids"])
                            csv_obj["segment_names"] = __compose_segment_names(user_segments, hull_obj["segment_ids"])
                    else:
                        # The key is not in this particular Hull object, so assume we have `null`
                        logger.info("Writing field %s with null value", key)
                        csv_obj[key] = None
                
                csvwriter.writerow(csv_obj.values())
            
    # Close the file
    tmp_file.close()
    logger.info("Completed to write to temporary file.")

    # Upload the file to S3 storage
    try:
        # Always instantiate the S3 client with a fixed api_version
        logger.info("Preparing to upload %s file to S3 storage...", S3_FILE_FORMAT.upper())
        s3_clnt = boto3.client("s3", api_version="2006-03-01")
        s3_file_name = f"{notification_id_safe}.{S3_FILE_FORMAT}"
        if S3_SINGLEFILE and not S3_DAILYFOLDER:
            s3_file_name = f"{S3_SINGLEFILE}.{S3_FILE_FORMAT}"
        elif S3_DAILYFOLDER and not S3_SINGLEFILE:
            if S3_DAILYFOLDER == "True" or S3_DAILYFOLDER == "true" or S3_DAILYFOLDER == "1":
                now = datetime.now(tz=timezone.utc)
                s3_file_name = f"{now:%Y-%m-%d}/{s3_file_name}"
        elif S3_DAILYFOLDER and S3_SINGLEFILE:
            if S3_DAILYFOLDER == "True" or S3_DAILYFOLDER == "true" or S3_DAILYFOLDER == "1":
                now = datetime.now(tz=timezone.utc)
                s3_file_name = f"{now:%Y-%m-%d}/{S3_SINGLEFILE}.{S3_FILE_FORMAT}"
            else:
                # Same as single-file, but we have to account for ops errors
                s3_file_name = f"{S3_SINGLEFILE}.{S3_FILE_FORMAT}"

        logger.info("Uploading temporary file /tmp/%s.%s to bucket %s with key %s", safe_name, S3_FILE_FORMAT, S3_BUCKET, s3_file_name)
        s3_clnt.upload_file(f'/tmp/{safe_name}.{S3_FILE_FORMAT}', S3_BUCKET, s3_file_name)
        logger.info("Upload to S3 completed. Deleting temporary file...")
        os.remove(f'/tmp/{safe_name}.{S3_FILE_FORMAT}')
        logger.info("Deleted temporary file.")
    except Exception as err:
        logger.error("An unhandled error occurred: %s", err)
        return {
            'statusCode': 500,
            'body': json.dumps(f"An unhandled error occurred: {err}")
        }
    else:
        # Indicate success
        logger.info("Successfully processed extract from Hull platform.")
        return {
            'statusCode': 200,
            'body': json.dumps("Successfully processed extract.")
        }
