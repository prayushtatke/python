from os import getenv
from utils.docdb_utils import Docdb
from utils.errors import *
from utils.logger import Logger
from utils.message_helper import gzipped_message_response, gzipped_object_response
import boto3
from botocore.exceptions import ClientError


LOG = Logger(__name__, getenv('LogLevel', 'DEBUG'))

s3 = None

def init_docdb(mock_client=None):
    global docdb, DOCDB_CONN_STR, DB_NAME, HF_DATA_COLL, ALARM_RPTS_COLL
    docdb.init()


def init():
    global is_init, docdb, s3, BUCKET_NAME
    if is_init:
        return
    try:
        init_docdb()
        BUCKET_NAME=getenv('BUCKET_NAME')
        s3 = boto3.client('s3')
    except Exception:
        LOG.error('unable to connect to Docdb')
        is_init = False
        return
    is_init = True


def handler(api_event, context):
    """
    Handles incoming lambda events
    :param event: rest event
    :param context: lambda context
    :return object representation of http response; see message_response
    """
    if not is_init:
        init()
        if not is_init:
            return
    return execute(api_event)


def execute(api_event):
    """
    Excecutes a Docdb query based based on Api Query Params
    :param api_event:
    :return:
    """
    LOG.debug(f'Validating the event {str(api_event)}')
    try:
      ids, file_type = validate_event(api_event)
    except InvalidRequestError as e:
        LOG.error(f'{str(e)}')
        return gzipped_message_response(400, str(e))

    query, proj= build_query(ids)
    LOG.debug(f'Executing Query: {str(query)}')
    try:
        if file_type in ['uff', 'kinx']:
            response = execute_query(HF_DATA_COLL, query, proj)
        else:
            response = execute_query(ALARM_RPTS_COLL, query, proj)

        return gzipped_object_response(200, response)
    except DataNotFoundError as e:
        LOG.error(f'{str(e)}')
        return gzipped_message_response(404, str(e))
    except Exception as e:
        LOG.error(f'Some Exception Occured while executing the query: {str(query)}')
        LOG.error(f'{str(e)}')
        LOG.info('Retrying one more time')
        init_docdb()
        try:
            response = execute_query(query)
            return gzipped_object_response(200, response)
        except Exception as e:
            return gzipped_message_response(500, str(e))


def validate_event(api_event):
    def raise_invalid_request_error(input_dict, key, err_msg=None):
        msg = err_msg
        if not msg:
            msg = f"No '{key}' param found."
        val = input_dict.get(key)
        if not val:
            raise InvalidRequestError(msg)
        return val

    event = raise_invalid_request_error(api_event, 'queryStringParameters', "No 'queryStringParameters' found." )
    ids = raise_invalid_request_error(event, 'ids')
    ids = ids.split(',')
    file_type = raise_invalid_request_error(event, 'file_type')
    return ids, file_type


def build_query(ids):
    query = {"_id" : {"$in" : ids }}
    query_proj = {"_id" : 0, "file_path" : 1}
    return query, query_proj


def execute_query(collection, query, proj):
    documents = docdb.find(collection, query, proj)
    num_docs, response = format_response(documents)
    LOG.debug(f'NumDocs : {num_docs},  Response : {str(response)}')
    if num_docs == 0:
        raise DataNotFoundError(f'No data found for query: {str(query)}')

    return response


def format_response(documents):
    response = []
    count = 0
    for doc in documents:
        count += 1
        path = doc.get('file_path')
        link = create_presigned_url(BUCKET_NAME, path)
        response.append(link)

    LOG.debug(str(response))
    return count, response

def create_presigned_url(bucket_name, object_name, expiration=1800):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    try:
        response = s3.generate_presigned_url('get_object',
                                            Params={'Bucket': bucket_name,
                                                    'Key': object_name},
                                            ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None
    return response

if __name__ == '__main__':
    import os
    os.environ = {
                  'LogLevel': 'DEBUG',
                  
                  }
    apievent = {
    "queryStringParameters" : {
      "ids": "id1,id2",
      "file_type": "pdf"
    }}
    handler(api_event=apievent, context=None)

