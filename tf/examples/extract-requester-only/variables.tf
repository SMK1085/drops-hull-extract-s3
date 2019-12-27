# ---------------------------------------------------------------------------------------------------------------------
# REQUIRED PARAMETERS
# You must provide a value for each of these parameters.
# ---------------------------------------------------------------------------------------------------------------------

variable "aws_region" {
  description = "The ID of the AWS region to deploy resources to"
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

variable "lambda_requester_callbackurl" {
    description = "The callback url to which the Hull platform will send the notification once the extract is ready."
}

variable "lambda_requester_esquery" {
    description = "The ElasticSearch query to match objects against which shall be extracted. Note: This must be valid stringified JSON."
}

variable "lambda_requester_fields" {
    description = "The list of fields or attributes to fetch for the matching objects. Note: This must be a valid stringified JSON array."
}



# ---------------------------------------------------------------------------------------------------------------------
# OPTIONAL PARAMETERS
# These parameters have reasonable defaults.
# ---------------------------------------------------------------------------------------------------------------------
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