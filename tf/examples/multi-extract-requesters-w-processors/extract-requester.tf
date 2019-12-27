# First Extract Requester Lambda
module "lambda_hull_extract_requester" {
  source = "../../modules/lambda-python"
  output_path = "lambda_hull_extract_requester.zip"
  description = var.lambda_requester1_description
  source_code_path = "${path.cwd}/../../../src/extract_requester"
  function_name = var.lambda_requester1_name
  handler_name = "extract_requester.handler"
  runtime          = "python3.7"

  event = {
    type                = "cloudwatch-scheduled-event"
    schedule_expression = var.lambda_requester1_schedule
  }

  tags =  var.lambda_requester1_tags

  environment = {
      variables = {
        "HULL_CONNECTOR_ID"       = var.lambda_requester1_hull_connectorid
        "HULL_CONNECTOR_SECRET"   = var.lambda_requester1_hull_connectorsecret
        "HULL_EXPORT_CALLBACKURL" = "${aws_api_gateway_deployment.hull_gw_prod.invoke_url}/${var.api_gw_resource_path1}" # Reference to api-gateway.tf
        "HULL_EXPORT_ESQUERY"     = jsonencode(var.lambda_requester1_esquery)
        "HULL_EXPORT_FIELDS"      = jsonencode(var.lambda_combined1_fields)
        "HULL_EXPORT_OBJECTTYPE"  = var.lambda_requester1_hull_objecttype
        "HULL_ORG_ID"             = var.lambda_requester1_hull_orgid
        "HULL_LOG_LEVEL"          = var.lambda_requester1_loglevel
      }
  }
}

# Enable cloudwatch-scheduled-event resource
module "event-cloudwatch-scheduled-event_hull_extract_requester" {
  source = "../../modules/events/cloudwatch-scheduled-event"
  enable = true
  lambda_function_arn = module.lambda_hull_extract_requester.arn
  schedule_expression = var.lambda_requester1_schedule
}

# Second Extract Requester Lambda
module "lambda_hull_extract_requester2" {
  source = "../../modules/lambda-python"
  output_path = "lambda_hull_extract_requester.zip"
  description = var.lambda_requester2_description
  source_code_path = "${path.cwd}/../../../src/extract_requester"
  function_name = var.lambda_requester2_name
  handler_name = "extract_requester.handler"
  runtime          = "python3.7"

  event = {
    type                = "cloudwatch-scheduled-event"
    schedule_expression = var.lambda_requester2_schedule
  }

  tags =  var.lambda_requester2_tags

  environment = {
      variables = {
        "HULL_CONNECTOR_ID"       = var.lambda_requester2_hull_connectorid
        "HULL_CONNECTOR_SECRET"   = var.lambda_requester2_hull_connectorsecret
        "HULL_EXPORT_CALLBACKURL" = "${aws_api_gateway_deployment.hull_gw_prod.invoke_url}/${var.api_gw_resource_path2}" # Reference to api-gateway.tf
        "HULL_EXPORT_ESQUERY"     = jsonencode(var.lambda_requester2_esquery)
        "HULL_EXPORT_FIELDS"      = jsonencode(var.lambda_combined2_fields)
        "HULL_EXPORT_OBJECTTYPE"  = var.lambda_requester2_hull_objecttype
        "HULL_ORG_ID"             = var.lambda_requester2_hull_orgid
        "HULL_LOG_LEVEL"          = var.lambda_requester2_loglevel
      }
  }
}

# Enable cloudwatch-scheduled-event resource
module "event-cloudwatch-scheduled-event_hull_extract_requester2" {
  source = "../../modules/events/cloudwatch-scheduled-event"
  enable = true
  lambda_function_arn = module.lambda_hull_extract_requester2.arn
  schedule_expression = var.lambda_requester2_schedule
}