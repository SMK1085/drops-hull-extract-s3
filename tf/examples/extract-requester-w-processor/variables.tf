# ---------------------------------------------------------------------------------------------------------------------
# REQUIRED PARAMETERS
# You must provide a value for each of these parameters.
# ---------------------------------------------------------------------------------------------------------------------

variable "aws_region" {
  description = "The ID of the AWS region to deploy resources to"
}

variable "lambda_processor_name" {
  description = "The unique name of your Extract Processor Lambda Function"
}

variable "lambda_requester_name" {
  description = "The unique name of your Extract Requester Lambda Function"
}

variable "lambda_requester_schedule" {
    description = "The scheduling expression on which to run the Extract Requester. For example, cron(0 20 * * ? *) or rate(5 minutes)."
}

variable "lambda_requester_hull_connectorid" {
    description = "The ID of your connector in Hull. Used to authenticate requests, you can pick any connector to obtain this value."
}

variable "lambda_requester_hull_connectorsecret" {
    description = "The secret of your connector in Hull. Used to authenticate requests, you can pick any connector to obtain this value."
}

variable "lambda_requester_hull_orgid" {
    description = "The ID of your organization in Hull. Used to route requests, you can pick any connector to obtain this value."
}

variable "lambda_requester_hull_objecttype" {
    description = "The type of objects to extract. Only `account` or `user` are supported."
}

variable "lambda_requester_esquery" {
    description = "The ElasticSearch query to match objects against which shall be extracted. Note: This must be valid stringified JSON."
    type        = any
}

variable "lambda_combined_fields" {
    description = "The list of fields or attributes to fetch via the extract include in the CSV. Note: This must be a valid JSON serializable list."
    type        = list(string)
}

variable "api_gw_name" {
    description = "The name of the API Gateway which serves the REST endpoint to invoke the Extract Processor Lambda Function"
}

variable "s3_bucket_name" {
    description = "The name of the S3 bucket. Can be an existing bucket."
}

# ---------------------------------------------------------------------------------------------------------------------
# OPTIONAL PARAMETERS
# These parameters have reasonable defaults.
# ---------------------------------------------------------------------------------------------------------------------
variable "lambda_processor_description" {
  description = "Description of what your Extract Requester Lambda Function"
  default     = "Hull Extract Requester: Requests an extract from Hull platform."
}

variable "lambda_processor_tags" {
  description = "A mapping of tags to assign to the Extract Requester Lambda function."
  type        = map(string)
  default     = {}
}

variable "lambda_processor_loglevel" {
    description = "The log level for your Extract Processor Lambda Function. Defaults to `ERROR`. To see full log output change it to `INFO`."
    default     = "ERROR"
}

variable "lambda_processor_timeout" {
    description = "The timeout in seconds for the Extract Processor Lambda Function. Defaults to max timeout of 15 minutes or 900 seconds."
    type        = number
    default     = 900
}

variable "lambda_processor_memory_size" {
  description = "The memory size in MB for the Extract Processor Lambda Function. Adjust according to the size of extracts. Defaults to 512 MB."
  default = "512"
}

variable "lambda_processor_dailyfolder" {
    description = "Enable or disable a daily folder. Default is disabled. Use `True` or `true` or `1` to enable"
    default = ""
}

variable "lambda_processor_fileformat" {
  description = "The file format to upload to the S3 bucket. Defaults to `csv`. Either `csv` or `json`"
  default = "csv"
}

variable "lambda_processor_singlefile" {
    description = "Enables a fixed file name. Default is disabled. Enter only the file name without extension."
    default = ""
}

variable "lambda_requester_description" {
  description = "Description of what your Extract Requester Lambda Function"
  default     = "Hull Extract Requester: Requests an extract from Hull platform."
}

variable "lambda_requester_tags" {
  description = "A mapping of tags to assign to the Extract Requester Lambda function."
  type        = map(string)
  default     = {}
}

variable "lambda_requester_loglevel" {
    description = "The log level for your Extract Requester Lambda Function. Defaults to `ERROR`. To see full log output change it to `INFO`."
    default     = "ERROR"
}

variable "api_gw_description" {
    description = "The description of the API Gateway which serves the REST endpoint to invoke the Extract Processor Lambda Function"
    default = "API Gateway to expose Lambda functions to integrate with Hull"
}

variable "api_gw_resource_path" {
    description = "The REST endpoint path to invoke the Extract Processor Lambda Function. Defaults to hull-extract-processor1"
    default = "hull-extract-processor1"
}

variable "api_gw_deployment_stage" {
    description = "The stage for the deployment of the API Gateway. Defaults to dev."
    default = "dev"
}

variable "s3_bucket_acl" {
    description = "The canned ACL to apply to the S3 bucket. Defaults to private."
    default = "private"
}

variable "s3_bucket_tags" {
  description = "A mapping of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}

variable "s3_bucket_lcr_enable" {
    description = "Enable or disable the lifecycle rule for extract files uploaded to the S3 bucket. Default is true."
    type        = bool
    default     = true
}

variable "s3_bucket_lcr_expiration_days" {
    description = "The expiration time in days for extract files uploaded to the S3 bucket. Default is 5 days."
    type        = number
    default     = 5
}