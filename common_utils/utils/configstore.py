import boto3
import json
import common_utils.utils.commons as util


class AWSParameterStoreException(Exception):
  pass

class AWSSecretKeyException(Exception):
  pass


class ConfigStore:

  @classmethod
  def get_config(cls, config_name, store_type='params', aws_region='eu-west-1'):
    if store_type == 'params':
      return ParamStore.get_params(config_name, aws_region=aws_region)
    elif store_type == 'secrets':
      return SecretManger.get_secrets(config_name, aws_region=aws_region)
    else:
      raise ValueError(f"Invalid 'store_type', should be 'param' or 'secrets', Current_value:{store_type}")


class ParamStore:

  @classmethod
  @util.raise_exception(throw=AWSParameterStoreException)
  def get_params(cls, param_name, aws_region='eu-west-1'):
    client = boto3.client(service_name='ssm',  region_name=aws_region)
    response = client.get_parameter(Name=param_name, WithDecryption=False)
    data = json.loads(response['Parameter']['Value'])
    return data


class SecretManger:

  @classmethod
  @util.raise_exception(throw=AWSSecretKeyException)
  def get_secrets(cls, secret_name, aws_region='eu-west-1'):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=aws_region)
    secret_values = client.get_secret_value(SecretId=secret_name)
    sm_resp = json.loads(secret_values['SecretString'])
    return sm_resp
