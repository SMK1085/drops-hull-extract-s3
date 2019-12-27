resource "aws_s3_bucket" "bucket_extracts" {
  bucket = var.s3_bucket_name
  acl    = var.s3_bucket_acl

  tags = var.s3_bucket_tags

  lifecycle_rule {
    id="lcr-hull-extracts"
    enabled = var.s3_bucket_lcr_enable
    expiration {
      days = var.s3_bucket_lcr_expiration_days
    }
  }
}

# Create Policy for the extractor lambda to access S3
resource "aws_iam_policy" "lambda_hull_extract_processor" {
  name = "HullExtractProcessorLambdaS3BucketAccess"
  description = "Grants the ${module.lambda_hull_extract_processor.function_name} full access to the given S3 bucket"
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": "${aws_s3_bucket.bucket_extracts.arn}*"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "lambda_hull_extractor_s3_access" {
  role       = module.lambda_hull_extract_processor.role_name   # Reference to the role_name output from the main module
  policy_arn = aws_iam_policy.lambda_hull_extract_processor.arn
}