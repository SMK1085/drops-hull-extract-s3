# Required settings
aws_region="us-east-1"
lambda_requester_name="hull_extract_requester1"
lambda_requester_schedule="rate(10 minutes)"
lambda_requester_hull_connectorid="YOUR_CONNECTOR_ID"
lambda_requester_hull_connectorsecret="YOUR_CONNECTOR_SECRET"
lambda_requester_hull_orgid="YOUR_NAMESPACE.hullapp.io"
lambda_requester_hull_objecttype="user"
lambda_requester_callbackurl="https://YOUR_BIN.x.pipedream.net/"
lambda_requester_esquery={"constant_score":{"filter":{"range":{"created_at":{"gt":"now-10m"}}}}}
lambda_requester_fields=["id","external_id","email","name"]

# Log level is optional, if you want to turn on detailed logs, uncomment the next line
# lambda_requester_loglevel="INFO"

# Description is optional, but highly recommended since the name of the Lambda might not be readable for humans
lambda_requester_description="Requests a user extract every 10 minutes and sends it to Pipedream"

# Tags are optional and only here to illustrate how to use them
lambda_requester_tags = {
    "Organization" = "Hull Inc."
    "Department" = "Solution Engineering"
    "Test" = true
    "Terraform" = true
}
