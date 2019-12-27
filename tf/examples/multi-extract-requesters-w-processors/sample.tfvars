# Required settings
aws_region="us-east-1"

lambda_requester1_name="hull_extract_requester1"
lambda_requester1_schedule="rate(10 minutes)"
lambda_requester1_hull_connectorid="YOUR_CONNECTOR_ID"
lambda_requester1_hull_connectorsecret="YOUR_CONNECTOR_SECRET"
lambda_requester1_hull_orgid="YOUR_NAMESPACE.hullapp.io"
lambda_requester1_hull_objecttype="user"
lambda_requester1_esquery={"constant_score":{"filter":{"range":{"created_at":{"gt":"now-10m"}}}}}

lambda_requester2_name="hull_extract_requester2"
lambda_requester2_schedule="rate(20 minutes)"
lambda_requester2_hull_connectorid="YOUR_CONNECTOR_ID"
lambda_requester2_hull_connectorsecret="YOUR_CONNECTOR_SECRET"
lambda_requester2_hull_orgid="YOUR_NAMESPACE.hullapp.io"
lambda_requester2_hull_objecttype="account"
lambda_requester2_esquery={"constant_score":{"filter":{"range":{"created_at":{"gt":"now-10m"}}}}}

lambda_processor1_name="hull_extract_processor1"
lambda_processor2_name="hull_extract_processor2"

lambda_combined1_fields=["id","external_id","email","name"] # Used for both, requester and processor to streamline the process
lambda_combined2_fields=["id","external_id","domain","name"] # Used for both, requester and processor to streamline the process

api_gw_name = "Hull Integration Gateway"

s3_bucket_name = "my-hull-extracts"

# Log level is optional, if you want to turn on detailed logs, uncomment the next line
# lambda_requester1_loglevel="INFO"
# lambda_requester2_loglevel="INFO"

# Description is optional, but highly recommended since the name of the Lambda might not be readable for humans
lambda_requester1_description="Requests a user extract every 10 minutes and sends it to the Processor Lambda 1"
lambda_requester2_description="Requests an account extract every 20 minutes and sends it to the Processor Lambda 2"

# Tags are optional and only here to illustrate how to use them
lambda_requester1_tags = {
    "Organization" = "Hull Inc."
    "Department" = "Solution Engineering"
    "Test" = true
    "Terraform" = true
}
lambda_requester2_tags = {
    "Organization" = "Hull Inc."
    "Department" = "Solution Engineering"
    "Test" = true
    "Terraform" = true
}

# Log level is optional, if you want to turn on detailed logs, uncomment the next line
# lambda_processor1_loglevel="INFO"
# lambda_processor2_loglevel="INFO"

# Description is optional, but highly recommended since the name of the Lambda might not be readable for humans
lambda_processor1_description = "Processes a user extract and turns it into a CSV"
lambda_processor2_description = "Processes an account extract and turns it into a CSV"

# Daily folder is optional, but is useful to find files more easily
lambda_processor1_dailyfolder = "True"   # Comment out if you want to disable this feature
# lambda_processor1_fileformat = "json"  # Uncomment to enable json format or explicitely specify it; default is csv.
# lambda_processor1_singlefile = "my-extract" # Uncomment if you want the Lambda to always upload files with this file name.
lambda_processor2_dailyfolder = "True"   # Comment out if you want to disable this feature
# lambda_processor2_fileformat = "json"  # Uncomment to enable json format or explicitely specify it; default is csv.
# lambda_processor2_singlefile = "my-extract" # Uncomment if you want the Lambda to always upload files with this file name.


# Tags are optional and only here to illustrate how to use them
lambda_processor1_tags = {
    "Organization" = "Hull Inc."
    "Department" = "Solution Engineering"
    "Test" = true
    "Terraform" = true
}
lambda_processor2_tags = {
    "Organization" = "Hull Inc."
    "Department" = "Solution Engineering"
    "Test" = true
    "Terraform" = true
}

# API Gateway has some sensible defaults, but for the sake of completion the defaults are listed here
api_gw_description = "API Gateway to expose Lambda functions to integrate with Hull"
api_gw_resource_path1 = "hull-extract-processor1" # This is the path parameter for the REST endpoint
api_gw_resource_path2 = "hull-extract-processor2" # This is the path parameter for the REST endpoint
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