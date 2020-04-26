# Important Commands
- Creating API container and starting API server locally.
> sam build --use-container
> sam local start-api

- Sam Packaging and deploy
> sam package --output-template-file deploy.yaml --s3-bucket 'sam.test'
> sam deploy --template-file deploy.yaml --region eu-west-1 \
> --parameter-overrides Stage=dev \
> --capabilities CAPABILITY_IAM \
> --stack-name 'awsapigwlambda_sam'
