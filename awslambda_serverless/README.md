## Overall Goal:
This is Lambda Function which will ingest data from raw input kinesis streams and will enrich the input stream with signals mapping data using customer name, customer asset id, source_system and signal_version.


## How It Does It:
**src.status_handler.handler**
Receives main event and initialises the implementer

**src.status.status.StatusFactory**
Provides implementer class as per vendor

**src.status_handler.KinesisLambdaHandler**
Provides a wraping class which 
- accepts the raw event, 
- parses the event to get the kinesis records
- call the implementor class for each record

**src.status.status.Status**
Abstract class for all the implementers.
- *update_status* for a payload record
- *fetch_asset_info* stored in Redis Cache
- check if needs to be processed by this lambda by *apply_filter*
- *calculate_status* from asset info and signal code in payload
- *save_status* to Redis Cache

Following Methods are abstract:
1. *get_status_code* (maps the signal code to status code)
2. *calculate_status* (maps the asset info to the status code)
3. *apply_filter* (checks if the record is to be processed by existing lambda)

**src.status.vestas_status.VestasStatusImplementer**
Implementer Class to process the Vestas Records from Kinesis


## Process:
1. Event is to be passed to *src.status_handler.handler*, which initialises the required wraping class.
2. *src.status.status.StatusFactory* will provide the implementer class that needs to be used as per the config in environment
3. *src.status_handler.KinesisLambdaHandler* uses the implementer class, for each record parsed.
4. The implementer class will first fetch the asset info from asset-metadata mapping from Redis.
5. The implementer class will then check if that record needs to be processed by this lambda.
6. Status code will be deduced as per *get_status_code* method
7. Deduces code will be stored under the asset_id key.


## Code Flow:
![picture](turbine_status_caching_service.png)

## Tech Stack:
- AWS Kinesis
- AWS Lambda
- Redis Cache


## Requirements:
### System Requirements:
- Python3.5 or above

### Python Library Requirements:
- boto3
- redis
- common_utils


## Environment Variable Common for all vendors 
| ENV_NAME | Value | Default |
| ------ | ------ | ------- |
| LOG_LEVEL | **********| INFO |
| REDIS_HOST | ********* |
| REDIS_PORT | ********* |
| REDIS_PASS_SECRET_KEY | ********* |
| SECRET_NAME | ********* |
| TURBINE_STATUS_MAPPING_KEY | *********** |
| ASSET_MAPPING_KEY | *********** |


### Environment Variable For Vestas
|ENV_NAME|Value| Description |
|------|------|--------|
|VMP_SIGNAL|*********| signal name for VMP |
|TAC_SIGNAL|*********| signal name for TAC |

##Roles Needed
* Roles Needed:
  - Redis Cache Access