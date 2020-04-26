## Important Commands
**Note:** 'sls' is alias of 'serverless', alias sls='serverless'
- Template to create aws lambda with Python
> sls create --template aws-python --name <lambda_name> --path </path/to/create/lambda>

- Invoking the lambda locally, with providing input data.
> sls invoke local --function <lambda_name> --data '{key1: val1}'

- Invoking the lambda locally, with providing input data as json file.
> sls invoke local --function <lambda_name> -p ../input.json

- To Package Lambda
> sls package --stage dev #OR
> sls package -s dev

- To Deploy Lambda
> sls deploy --stage dev #OR
> sls deploy -s dev

- To Deploy Lambda with user defined params.
Below 'env' is defined as 'opt' variable in serverless.yml.
> sls deploy --env dev --version 1.1.2


## Overall Goal:
This is Lambda Function which will ingest data from raw input kinesis streams and will enrich the input.

## How:
**src.status_handler.handler**
Receives main event and initialises the implementer

**src.status.status.StatusFactory**
Provides implementer class as per env

**src.status_handler.KinesisLambdaHandler**
Provides a wraping class which
- accepts the raw event
- parses the event to get the kinesis records
- call the implementor class for each record

Following Methods are abstract:
1. *apply_filter* (checks whether payload to be processed.)
2. *enrich* (enriches the payload)

## Process:
1. Event is to be passed to *src.status_handler.handler*, which initialises the required wraping class.
2. *src.status.status.StatusFactory* will provide the implementer class that needs to be used as per the config in environment
3. *src.status_handler.KinesisLambdaHandler* uses the implementer class, for each record parsed.
5. The implementer class will then check if that record needs to be processed by this lambda.
6. Status code will be deduced as per *get_status_code* method


## Tech Stack:
- AWS Kinesis
- AWS Lambda
- Redis Cache


## Requirements:
### System Requirements:
- Python3.7 or above

### Python Library Requirements:
- boto3
- common_utils


## Environment Variable Common for all vendors
| ENV_NAME | Value | Default |
| ------ | ------ | ------- |
| LOG_LEVEL | **********| INFO |
