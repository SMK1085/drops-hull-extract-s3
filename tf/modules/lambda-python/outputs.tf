output "arn" {
  description = "The Amazon Resource Name (ARN) identifying your Lambda Function."
  value       = aws_lambda_function.lambda_python.arn
}

output "function_name" {
  description = "The unique name of your Lambda Function."
  value       = aws_lambda_function.lambda_python.function_name
}

output "invoke_arn" {
  description = "The ARN to be used for invoking Lambda Function from API Gateway - to be used in aws_api_gateway_integration's uri"
  value       = aws_lambda_function.lambda_python.invoke_arn
}

output "role_name" {
  description = "The name of the IAM attached to the Lambda Function."
  value       = aws_iam_role.lambda.name
}

