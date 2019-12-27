# ---------------------------------------------------------------------------------------------------------------------
# REQUIRED PARAMETERS
# You must provide a value for each of these parameters.
# ---------------------------------------------------------------------------------------------------------------------

variable "function_name" {
  description = "A unique name for your Lambda Function"
}

variable "handler_name" {
  description = "The function entrypoint in your code."
}

variable "source_code_path" {
  description = "Path to the source file or directory containing your Lambda source code & requirements.txt if applicable"
}

variable "output_path" {
  description = "Path to the function's deployment package within local filesystem. eg: /path/to/lambda.zip"
}

variable "runtime" {
  description = "The runtime environment for the Lambda function you are uploading."
}
# ---------------------------------------------------------------------------------------------------------------------
# OPTIONAL PARAMETERS
# These parameters have reasonable defaults.
# ---------------------------------------------------------------------------------------------------------------------
variable "description" {
  description = "Description of what your Lambda Function does."
  default     = ""
}

variable "environment" {
  description = "Environment (e.g. env variables) configuration for the Lambda function enable you to dynamically pass settings to your function code and libraries"
  type        = map(map(string))
  default     = {}
}

variable "memory_size" {
  description = "Amount of memory in MB your Lambda Function can use at runtime."
  default     = "128"
}

variable "publish" {
  description = "Whether to publish creation/change as new Lambda Function Version. Defaults to false."
  default     = false
}

variable "reserved_concurrent_executions" {
  description = "The amount of reserved concurrent executions for this lambda function. A value of 0 disables lambda from being triggered and -1 removes any concurrency limitations. Defaults to Unreserved Concurrency Limits -1."
  default     = "-1"
}

variable "tags" {
  description = "A mapping of tags to assign to the Lambda function."
  type        = map(string)
  default     = {}
}

variable "timeout" {
  description = "The amount of time your Lambda Function has to run in seconds. Defaults to 5 minutes."
  default     = 300
}

variable "vpc_config" {
  description = "Provide this to allow your function to access your VPC (if both 'subnet_ids' and 'security_group_ids' are empty then vpc_config is considered to be empty or unset, see https://docs.aws.amazon.com/lambda/latest/dg/vpc.html for details)."
  type        = map(list(string))
  default     = {}
}

variable "event" {
  description = "Event source configuration which triggers the Lambda function. Supported events: cloudwatch-scheduled-event, dynamodb, s3, sns"
  type        = map(string)
  default     = {}
}