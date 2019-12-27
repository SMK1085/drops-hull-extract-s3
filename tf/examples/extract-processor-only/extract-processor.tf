module "lambda_hull_extract_processor" {
  source           = "../../modules/lambda-python"
  output_path      = "lambda_hull_extract_processor.zip"
  description      = var.lambda_processor_description
  source_code_path = "${path.cwd}/../../../src/extract_processor"
  function_name    = var.lambda_processor_name
  handler_name     = "extract_processor.handler"
  runtime          = "python3.7"
  timeout          = var.lambda_processor_timeout
  memory_size      = var.lambda_processor_memory_size
  
  tags = var.lambda_processor_tags

  environment = {
      variables = {
        "S3_BUCKET"               = var.s3_bucket_name
        "S3_DAILYFOLDER"          = var.lambda_processor_dailyfolder
        "S3_FILE_FORMAT"          = var.lambda_processor_fileformat
        "S3_SINGLEFILE"           = var.lambda_processor_singlefile
        "HULL_EXPORT_FIELDS"      = jsonencode(var.lambda_processor_fields)
        "HULL_LOG_LEVEL"          = var.lambda_processor_loglevel
      }
  }
}