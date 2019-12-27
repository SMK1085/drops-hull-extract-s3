resource "aws_api_gateway_rest_api" "hull_gw" {
  name        = var.api_gw_name
  description = var.api_gw_description
}

resource "aws_api_gateway_resource" "hull_gw_proxy" {
   rest_api_id = aws_api_gateway_rest_api.hull_gw.id
   parent_id   = aws_api_gateway_rest_api.hull_gw.root_resource_id
   path_part   = var.api_gw_resource_path1
}

resource "aws_api_gateway_resource" "hull_gw_proxy2" {
   rest_api_id = aws_api_gateway_rest_api.hull_gw.id
   parent_id   = aws_api_gateway_rest_api.hull_gw.root_resource_id
   path_part   = var.api_gw_resource_path2
}

resource "aws_api_gateway_method" "hull_gw_proxy" {
   rest_api_id   = aws_api_gateway_rest_api.hull_gw.id
   resource_id   = aws_api_gateway_resource.hull_gw_proxy.id
   http_method   = "POST"
   authorization = "NONE"
 }

 resource "aws_api_gateway_method" "hull_gw_proxy2" {
   rest_api_id   = aws_api_gateway_rest_api.hull_gw.id
   resource_id   = aws_api_gateway_resource.hull_gw_proxy2.id
   http_method   = "POST"
   authorization = "NONE"
 }

resource "aws_api_gateway_integration" "lambda_hull_extract_processor" {
    rest_api_id = aws_api_gateway_rest_api.hull_gw.id
    resource_id = aws_api_gateway_method.hull_gw_proxy.resource_id
    http_method = aws_api_gateway_method.hull_gw_proxy.http_method

    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = module.lambda_hull_extract_processor.invoke_arn # reference to the ARN in main module
}

resource "aws_api_gateway_integration" "lambda_hull_extract_processor2" {
    rest_api_id = aws_api_gateway_rest_api.hull_gw.id
    resource_id = aws_api_gateway_method.hull_gw_proxy2.resource_id
    http_method = aws_api_gateway_method.hull_gw_proxy2.http_method

    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = module.lambda_hull_extract_processor2.invoke_arn # reference to the ARN in main module
}

resource "aws_api_gateway_deployment" "hull_gw_prod" {
   depends_on = [
     aws_api_gateway_integration.lambda_hull_extract_processor,
     aws_api_gateway_integration.lambda_hull_extract_processor2
   ]

   rest_api_id = aws_api_gateway_rest_api.hull_gw.id
   stage_name  = var.api_gw_deployment_stage
 }

 resource "aws_lambda_permission" "hull_gw_perm_lambda_hull_extract_processor" {
   statement_id  = "AllowAPIGatewayInvoke"
   action        = "lambda:InvokeFunction"
   function_name = module.lambda_hull_extract_processor.function_name # reference to the function name in main module
   principal     = "apigateway.amazonaws.com"

   # The "/*/*" portion grants access from any method on any resource
   # within the API Gateway REST API.
   source_arn = "${aws_api_gateway_rest_api.hull_gw.execution_arn}/*/*"
 }

 resource "aws_lambda_permission" "hull_gw_perm_lambda_hull_extract_processor2" {
   statement_id  = "AllowAPIGatewayInvoke"
   action        = "lambda:InvokeFunction"
   function_name = module.lambda_hull_extract_processor2.function_name # reference to the function name in main module
   principal     = "apigateway.amazonaws.com"

   # The "/*/*" portion grants access from any method on any resource
   # within the API Gateway REST API.
   source_arn = "${aws_api_gateway_rest_api.hull_gw.execution_arn}/*/*"
 }