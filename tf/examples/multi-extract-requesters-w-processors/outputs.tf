output "api_gw_base_url" {
    description="The base url of the API Gateway which exposes the Extract Processor Lambda"
    value = aws_api_gateway_deployment.hull_gw_prod.invoke_url
}

output "api_gw_extract_processor_url1" {
    description="The base url of the API Gateway which exposes the first Extract Processor Lambda"
    value = "${aws_api_gateway_deployment.hull_gw_prod.invoke_url}/${var.api_gw_resource_path1}"
}

output "api_gw_extract_processor_url2" {
    description="The base url of the API Gateway which exposes the second Extract Processor Lambda"
    value = "${aws_api_gateway_deployment.hull_gw_prod.invoke_url}/${var.api_gw_resource_path2}"
}