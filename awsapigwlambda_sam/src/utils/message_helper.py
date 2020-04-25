"""
Utility for formatting API responses.
"""

import gzip
import json
import base64

def gzipped_message_response(status_code, message):
    """
    Create a response containing a single string message.
    :param status_code: response status code
    :param message: message
    :return: object representation of API response
    """
    return gzipped_object_response(status_code, {
        'message': message
    })


def gzipped_object_response(status_code, body):
    """
    Create a response containing an object body
    :param status_code: response status code
    :param body: object to json formatted as the response body
    :return: object representation of cms-file-apis response
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Encoding': 'gzip'
        },
        'isBase64Encoded': True,
        'body': base64.b64encode(gzip.compress(json.dumps(body).encode(), 1)).decode()
    }
def gunzip_response_body(zipped_response_body):
    """
    Unzips a previously zipped response body
    :param zipped_response_body: the previously zipped response body
    :return the unzipped and json loaded response body object
    """
    gunzipped_object = gzip.decompress(base64.b64decode(zipped_response_body)).decode()
    return json.loads(gunzipped_object)