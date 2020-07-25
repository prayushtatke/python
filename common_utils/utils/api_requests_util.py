import time
import requests
from requests.exceptions import RequestException
from common_utils.utils.logger import Logger

log = Logger('API Requester')

class ApiRequesterInvalidResponse(RequestException):
    pass


def post(url, data):
    try:
        r = requests.post(url=url, data=data)
        return r, False
    except Exception as e:
        return None, e


def post_api(api_endpoint, api_key, data_config, retry=3, retry_time=30):
    data = {
        "token": api_key
    }

    data.update(data_config)

    resp, error = post(api_endpoint, data)
    retry_c = 0
    while retry_c < retry:
        if not resp or error:
            retry_c += 1
            log.warning(f'API invoke error: {str(error)}; data: {data_config}, Retrying {retry_c}(of {retry}), Retry interval: {retry_time} Secs')
            time.sleep(retry_time)
        elif resp.status_code != 200:
            retry_c += 1
            api_resp = {
                       'headers': resp.headers,
                       'content': resp.content,
                       'post_data': data_config
                       }
            log.warning(
                f'API Responded with: {str(resp.status_code)}, API Details: {str(api_resp)}, Retrying {retry_c}(of {retry}), Retry interval: {retry_time} Secs')
            time.sleep(retry_time)
        else:
            # when API responded successfully, status_code == 200
            log.info(f'Response Details: [ Headers :{resp.headers}, Length: {len(resp.content)}; Data_From : {data_config["from"]}; Data_To : {data_config["to"]}]')
            return resp.json()

        resp, error = post(api_endpoint, data)

    if error:
        raise error

    # Unlikely
    if resp is None:
        raise RequestException(f'Empty Response')

    if resp.status_code != 200:
        api_resp = {
            'status' : resp.status_code,
            'headers': resp.headers,
            'content': resp.content,
            'post_data': data_config
        }
        raise RequestException(f'Invalid Response: {str(api_resp)}')
