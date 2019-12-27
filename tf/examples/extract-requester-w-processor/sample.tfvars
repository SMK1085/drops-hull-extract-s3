# Required settings
aws_region="us-east-1"

lambda_requester_name="hull_extract_requester1"
lambda_requester_schedule="rate(10 minutes)"
lambda_requester_hull_connectorid="YOUR_CONNECTOR_ID"
lambda_requester_hull_connectorsecret="YOUR_CONNECTOR_SECRET"
lambda_requester_hull_orgid="YOUR_NAMESPACE.hullapp.io"
lambda_requester_hull_objecttype="user"
lambda_requester_esquery={"constant_score":{"filter":{"range":{"created_at":{"gt":"now-10m"}}}}}

lambda_processor_name="hull_extract_processor1"

lambda_combined_fields=["id","external_id","email","name"] # Used for both, requester and processor to streamline the process

api_gw_name = "Hull Integration Gateway"

s3_bucket_name = "my-hull-extracts"

# Log level is optional, if you want to turn on detailed logs, uncomment the next line
# lambda_requester_loglevel="INFO"

# Description is optional, but highly recommended since the name of the Lambda might not be readable for humans
lambda_requester_description="Requests a user extract every 10 minutes and sends it to the Processor Lambda"

# Tags are optional and only here to illustrate how to use them
lambda_requester_tags = {
    "Organization" = "Hull Inc."
    "Department" = "Solution Engineering"
    "Test" = true
    "Terraform" = true
}

# Log level is optional, if you want to turn on detailed logs, uncomment the next line
# lambda_processor_loglevel="INFO"

# Description is optional, but highly recommended since the name of the Lambda might not be readable for humans
lambda_processor_description = "Processes a user extract and turns it into a CSV"

# Daily folder is optional, but is useful to find files more easily
lambda_processor_dailyfolder = "True"   # Comment out if you want to disable this feature
# lambda_processor_fileformat = "json"  # Uncomment to enable json format or explicitely specify it; default is csv.
# lambda_processor_singlefile = "my-extract" # Uncomment if you want the Lambda to always upload files with this file name.

# Tags are optional and only here to illustrate how to use them
lambda_processor_tags = {
    "Organization" = "Hull Inc."
    "Department" = "Solution Engineering"
    "Test" = true
    "Terraform" = true
}

# API Gateway has some sensible defaults, but for the sake of completion the defaults are listed here
api_gw_description = "API Gateway to expose Lambda functions to integrate with Hull"
api_gw_resource_path = "hull-extract-processor1" # This is the path parameter for the REST endpoint
api_gw_deployment_stage = "dev" # This is the stage definition for the API Gateway, typically `dev`, `testing` or `prod`

# S3 Bucket has some sensible defaults, variables are only listed to illustrate how to use them
s3_bucket_acl = "private"
s3_bucket_tags = {
    "Organization" = "Hull Inc."
    "Department" = "Solution Engineering"
    "Test" = true
    "Terraform" = true
}
s3_bucket_lcr_enable = true # Enable lifecycle rule to automatically expire old files
s3_bucket_lcr_expiration_days = 5 # Set expiration time of old files to 5 days; has no effect if `s3_bucket_lcr_enable` is set to `false`