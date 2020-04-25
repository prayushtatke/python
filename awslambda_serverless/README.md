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

