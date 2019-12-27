# Example Extract Processor Only

> Note: This example might create resources which can cost money. Run `terraform destroy` when you don't need the resources.

Running this example with Terraform will create the `Extract Processor Lambda` function only, with the necessary dependencies of an AWS API Gateway and S3 bucket along with the necessary permissions.

## Usage

Make sure that you are in this directory (not the root directory) before executing any of the commands below.
Also, the next steps require the AWS CLI to be configured properly. See the documentation from AWS for details.

Copy the `sample.tfvars` file to `test.tfvars` (or any other name you like):

```bash
cp sample.tfvars test.tfvars
```

Inside the `test.tfvars` make sure to replace the variables with the ones from your individual setup; otherwise you can deploy the resources to AWS but the execution will fail.

Initialize Terraform, if you haven't already done so, using:

```bash
terraform init
```

Now **terraform plan** the deployment using:

```bash
terraform plan --out=extract-processor-only.plan -var-file=test.tfvars
```

Note: The above command creates a `.plan` file so you can call `terraform apply` later. You can omit the `--out` parameter tough, if you prefer to not save the plan. See the Terraform documentation for further details about this parameter. The `-var-file` parameter takes the file reference of the variables file you copied earlier. If you have used a different name, make sure to adjust the command accordingly.

If the output from plan looks good, we can go ahead and perform **terraform apply** using:

```bash
terraform apply "extract-processor-only.plan"
```

After a short amount of time you should see the resources in your AWS dashboard. Once the CloudWatch event triggers, you can verify the execution in the logs of your Lambda function. Once the Hull platform has created the extract, the specified callback url will be invoked with the extract response.

Once you are done testing or want to destroy the configuration, invoke:

```bash
terraform plan -var-file=test.tfvars
```

Note: The `-var-file` parameter takes the file reference of the variables file you copied earlier. If you have used a different name, make sure to adjust the command accordingly.

## Troubleshooting

The `Extract Processor Lambda` has full logging capabilities built-in. By default the log level is set to `ERROR`, however you can turn on detailed logs by setting the `lambda_processor_loglevel` variable to `INFO`. This will output step by step logs including configuration which should help you troubleshoot the problem further.
