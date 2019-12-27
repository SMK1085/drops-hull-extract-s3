module "lambda_hull_extract_requester" {
  source = "../../modules/lambda-python"
  output_path = "lambda_hull_extract_requester.zip"
  description = var.lambda_requester_description
  source_code_path = "${path.cwd}/../../../src/extract_requester"
  function_name = var.lambda_requester_name
  handler_name = "extract_requester.handler"
  runtime          = "python3.7"

  event = {
    type                = "cloudwatch-scheduled-event"
    schedule_expression = var.lambda_requester_schedule
  }

  tags =  var.lambda_requester_tags

  environment = {
      variables = {
        "HULL_CONNECTOR_ID"       = var.lambda_requester_hull_connectorid
        "HULL_CONNECTOR_SECRET"   = var.lambda_requester_hull_connectorsecret
        "HULL_EXPORT_CALLBACKURL" = var.lambda_requester_callbackurl
        "HULL_EXPORT_ESQUERY"     = jsonencode(var.lambda_requester_esquery)
        "HULL_EXPORT_FIELDS"      = jsonencode(var.lambda_requester_fields)
        "HULL_EXPORT_OBJECTTYPE"  = var.lambda_requester_hull_objecttype
        "HULL_ORG_ID"             = var.lambda_requester_hull_orgid
        "HULL_LOG_LEVEL"          = var.lambda_requester_loglevel
      }
  }
}

# Enable cloudwatch-scheduled-event resource
module "event-cloudwatch-scheduled-event_hull_extract_requester" {
  source = "../../modules/events/cloudwatch-scheduled-event"
  enable = true
  lambda_function_arn = module.lambda_hull_extract_requester.arn
  schedule_expression = var.lambda_requester_schedule
}