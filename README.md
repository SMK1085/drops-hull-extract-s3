# drops-hull-extract-s3

[![License](https://img.shields.io/github/license/SMK1085/drops-hull-extract-s3.svg?style=flat-square)](https://github.com/SMK1085/drops-hull-extract-s3/blob/master/LICENSE) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/SMK1085/drops-hull-extract-s3#can-i-contribute-code) [![Code of conduct](https://img.shields.io/badge/code%20of-conduct-ff69b4.svg?style=flat-square)](https://github.com/SMK1085/drops-hull-extract-s3/blob/master/CODE_OF_CONDUCT.md)

A DROPS for requesting an extract from Hull and uploading it to AWS S3.

## Business Problem

This DROPS provides a sample solution to achieve the goal of periodically requesting extracts from the Hull platform and storing the result as CSV or JSON file in S3 to perform analysis or other tasks on the data.

## Solution Overview

This DROPS consists of two AWS Lambda functions which are written in Python. To deploy the sample solution easily, Terraform modules are available to provision all required AWS resources including the API Gateway, the S3 bucket and the necessary permissions, following the least privileged principle.

### Extract Requester Function

The purpose of this Lambda function is to request an extract from the Hull platform and is meant to be invoked via a scheduled event from AWS CloudWatch.
Since scheduled events do not carry any information, the configuration of what extract to ask for is done using environment variables of the Lambda function. The following variables are available:

| Variable | Description | Notes |
| -------- | ----------- | ----- |
|`HULL_CONNECTOR_ID`| The ID of the connector | Used to authenticate the extract request. Get it from any connector in your Hull organization |
|`HULL_CONNECTOR_SECRET`| The Secret of the connector | Used to authenticate the extract request. Get it from any connector in your Hull organizaton |
|`HULL_ORG_ID`| The ID of your Hull organization | This is the full ID of your Hull organization, e.g. `demo.hullapp.io`. Get it from any connector in your Hull organization |
|`HULL_EXPORT_CALLBACKURL`| The url of the Extract Processor Lambda Function | The url of the API Gateway Method to invoke the Extract Processor Function |
|`HULL_EXPORT_OBJECTTYPE`| The type of object to export. | Currently only `user` or `account` are supported.
|`HULL_EXPORT_FIELDS`| The fields to export in JSON encoded format. | Expects an array of fields, e.g. `["id", "external_id", "email", "hubspot/id"]`|
|`HULL_EXPORT_ESQUERY`| The ElasticSearch query to match objects against. | Expects a valid ElasticSearch query.|
|`HULL_LOG_LEVEL`| Optional. Defines the log level. | See section [Logging](#Logging) for details. |

### Extract Processor Function

The purpose of this Lambda function is to download the extracted file made available by the Hull platform and to handle the upload to S3.
This function requires a configured API Gateway method and access to the S3 bucket to upload the resulting files.

To configure the behavior, the following environment variables are available:

| Variable | Description | Notes |
| -------- | ----------- | ----- |
|`S3_BUCKET`| The name of the S3 bucket. | Note that the function needs to have permissions to at least upload files. |
|`S3_SINGLEFILE`| Optional. The name of the file to upload without extension.| You should set this variable only if you either want to overwrite the existing file (when `S3_DAILYFOLDER` is either not set or set to `False`) or if you want a consistent file name in your daily folder. |
|`S3_DAILYFOLDER`| Optional. Set it to `True`, `true` or `1` to enable a daily folder.| If this setting is enabled, the Lambda function will create a folder per day in the format YYYY-MM-DD, e.g. for Dec 26, 2019 it will create a folder named `2019-12-26` and add the resulting file to it. The day is determined by the UTC time when the function is invoked.|
|`S3_FILE_FORMAT`| Optional. Either `csv` or `json`, default is `csv`| Defines the file format to store data in. If not set it defaults to `csv`.|
|`HULL_EXPORT_FIELDS`| Optional. The fields to include in the S3 file in JSON encoded format. | Expects an array of fields, e.g. `["id", "external_id", "email", "hubspot/id"]`. If this variable is not set and the `S3_FILE_FORMAT` is set to `csv`, the first object in the extract will be used to determine the columns in the CSV file. This might lead to missing columns, so it is advised to keep the fields between the Requester and Processor functions in sync. If the `S3_FILE_FORMAT` is set to `json`, this parameter will be ignored. |
|`HULL_LOG_LEVEL`| Optional. Defines the log level. | See section [Logging](#Logging) for details. |

### Logging

Both Lambda functions come with logging, using the [logging library](https://docs.python.org/3/library/logging.html) from Python. If no log level is specified, the logger assumes a production environment and the log level will default to `ERROR`. To trace problems down, it is recommended to set the log level to `INFO` which will cause the functions to log every step with the relevant configuration. For further details about the output and how to retrieve the logs using CloudWatch, please refer to the [AWS documentation](https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html).

## Deployment using Terraform

### Requirements

Make sure that you have Terraform v0.12.0 or higher installed on your computer. You can download the latest version from the [Terraform download page](https://www.terraform.io/downloads.html).

### Examples

This repository contains various samples to get you started quickly with deploying everything to AWS. See the [Terraform examples folder](./tf/examples) for common quickstart scenarios:

| Scenario | Description |
| -------- | ----------- |
| [`extract-requester-only`](./tf/examples/extract-requester-only/README.md) | This scenario deploys a Lambda function which can request extracts from the Hull platform along with a CloudWatch scheduled event, so it can be executed on the defined schedule. |
| [`extract-processor-only`](./tf/examples/extract-processor-only/README.md) | This scenario deploys a Lambda function which can process extracts from the Hull platform along with the required API Gateway and S3 bucket. It also assigns IAM permissions to make all components work with each other. |

Please refer to the respective READMEs of each scenario to learn how to deploy the scenario using Terraform. All code examples are configurable by adjusting the `.tfvars` files to your needs. All variables are described in the corresponding `variables.tf` file.

## Inspiration

- [terraform_aws_lambda_python](https://github.com/ruzin/terraform_aws_lambda_python)
- [blog-lambda-unit-testing-python](https://github.com/binxio/blog-lambda-unit-testing-python)
- [Introducing DROPS](https://medium.com/@smaschek85/introducing-drops-to-improve-dx-and-cx-for-saas-39a20f6e0f40)

## Credits

This project is authored and maintained by Sven Maschek ([@smaschek85](https://medium.com/@smaschek85) / [@svenmaschek](https://twitter.com/svenmaschek)).

Thank you to all [contributors](https://github.com/SMK1085/drops-hull-extract-s3/graphs/contributors).

## License

Open-source under [MIT License](https://github.com/SMK1085/drops-hull-extract-s3/blob/master/LICENSE).

## FAQ

### Uh oh, something went wrong!

Sorry about that. Please submit a bug report using the [GitHub issue tracker](https://github.com/SMK1085/drops-hull-extract-s3/issues).

### I wish something was different…

Keen to hear all ideas! Create an enhancement request using the [GitHub issue tracker](https://github.com/SMK1085/drops-hull-extract-s3/issues).

### Can I contribute code?

Yes please! See [CONTRIBUTING.md](./CONTRIBUTING.md) and [DEVELOPING.md](./DEVELOPING.md).

### My question isn't answered :(

Ask away using the [GitHub issue tracker](https://github.com/SMK1085/drops-hull-extract-s3/issues).
