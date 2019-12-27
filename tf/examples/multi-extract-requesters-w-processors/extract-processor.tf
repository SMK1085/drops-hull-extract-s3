# The first extract processor
module "lambda_hull_extract_processor" {
  source           = "../../modules/lambda-python"
  output_path      = "lambda_hull_extract_processor.zip"
  description      = var.lambda_processor1_description
  source_code_path = "${path.cwd}/../../../src/extract_processor"
  function_name    = var.lambda_processor1_name
  handler_name     = "extract_processor.handler"
  runtime          = "python3.7"
  timeout          = var.lambda_processor1_timeout
  memory_size      = var.lambda_processor1_memory_size
  
  tags = var.lambda_processor1_tags

  environment = {
      variables = {
        "S3_BUCKET"               = var.s3_bucket_name
        "S3_DAILYFOLDER"          = var.lambda_processor1_dailyfolder
        "S3_FILE_FORMAT"          = var.lambda_processor1_fileformat
        "S3_SINGLEFILE"           = var.lambda_processor1_singlefile
        "HULL_EXPORT_FIELDS"      = jsonencode(var.lambda_combined1_fields)
        "HULL_LOG_LEVEL"          = var.lambda_processor1_loglevel
      }
  }
}

# The second extract processor
module "lambda_hull_extract_processor2" {
  source           = "../../modules/lambda-python"
  output_path      = "lambda_hull_extract_processor.zip"
  description      = var.lambda_processor2_description
  source_code_path = "${path.cwd}/../../../src/extract_processor"
  function_name    = var.lambda_processor2_name
  handler_name     = "extract_processor.handler"
  runtime          = "python3.7"
  timeout          = var.lambda_processor2_timeout
  memory_size      = var.lambda_processor2_memory_size
  
  tags = var.lambda_processor2_tags

  environment = {
      variables = {
        "S3_BUCKET"               = var.s3_bucket_name
        "S3_DAILYFOLDER"          = var.lambda_processor2_dailyfolder
        "S3_FILE_FORMAT"          = var.lambda_processor2_fileformat
        "S3_SINGLEFILE"           = var.lambda_processor2_singlefile
        "HULL_EXPORT_FIELDS"      = jsonencode(var.lambda_combined2_fields)
        "HULL_LOG_LEVEL"          = var.lambda_processor2_loglevel
      }
  }
}