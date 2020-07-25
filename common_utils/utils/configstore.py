import boto3
import json
from json.decoder import JSONDecodeError
import common_utils.utils.commons as util
from common_utils.utils.decorators import raise_exception, retry


class AWSParameterStoreException(Exception):
  pass

class AWSSecretKeyException(Exception):
  pass


class ConfigStore:

  @classmethod
  def get_config(cls, config_name, store_type='params', aws_region='eu-west-1', secured=False):
    if store_type == 'params':
      return ParamStore.get_params(config_name, aws_region=aws_region, secured=secured)
    elif store_type == 'secrets':
      return SecretManger.get_secrets(config_name, aws_region=aws_region)
    else:
      raise ValueError(f"Invalid 'store_type', should be 'params' or 'secrets', Current_value:{store_type}")


class ParamStore:

  @classmethod
  @retry(tries=3, delay=2)
  @raise_exception(throw=AWSParameterStoreException)
  def get_params(cls, param_name, aws_region='eu-west-1', secured=False):
    client = boto3.client(service_name='ssm',  region_name=aws_region)
    response = client.get_parameter(Name=param_name, WithDecryption=secured)
    try:
      data = json.loads(response['Parameter']['Value'])
    except JSONDecodeError as e:
      data = response['Parameter']['Value']
    return data


class SecretManger:

  @classmethod
  @retry(tries=3, delay=2)
  @raise_exception(throw=AWSSecretKeyException)
  def get_secrets(cls, secret_name, aws_region='eu-west-1'):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=aws_region)
    secret_values = client.get_secret_value(SecretId=secret_name)
    sm_resp = json.loads(secret_values['SecretString'])
    return sm_resp
