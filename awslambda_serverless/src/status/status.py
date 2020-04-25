import sys, os

sys.path.append(os.path.realpath('../'))
import json
from abc import abstractmethod
from common_utils.utils.commons import get_logger, find_missing_or_empty_keys

log = get_logger(__name__, log_level=LOG_LEVEL, log_format=LOG_FORMAT)


class StatusImplementationError(Exception):
    pass


class Status:
    def __init__(self, config: dict, mock_client=None):
        """

        :param config: configuration required for class instance.
                 redis_info_param_name: Parameter Name for Redis Connection
        :param mockclient: fakeredis.FakeServer for mock testing of the implementors
        """
        

    @abstractmethod
    def get_status_code(self, ttype, status_val) -> str:
        """
        Get the status code as per ttype and it's status_val
        :param status_val: str
        """
        # get the status code from __status_code or __default_code
        pass

    @abstractmethod
    def apply_filter(self, payload: dict, ainfos) -> (dict, dict):
        """
        To check if payload to be processed with this lambda
        """
        # check if needs to process by this lambda
        pass

    @abstractmethod
    def enrich(self, ainfos, payloads) -> dict:
        """ 
        :param payload: Kinesis Payload
        """
        pass
    

    def enrich_payload(self, payload) -> None:
        """
        Process Kinesis Record and save to Redis Cache
        :param payload: Kinesis Records
        """
        filtered_payloads = self.apply_filter(payload)
        enriched = self.enrich(filtered_payloads)
        return enriched

        

class StatusFactory:
    status_impls = {'vestas,suzlon': 'dummy_status.DummyStatusImpl'
                    }

    @classmethod
    def get_status_impl(cls, cust_name) -> Status:
        fpath = cls.status_impls.get(cust_name)
        if not fpath:
            raise StatusImplementationError(f"No Implementation found for '{cust_name}'")

        file, clazz = fpath.split('.')

        try:
            # Loading Module
            mod = __import__(f'src.status.{file}')
            # loading class
            impl = getattr(getattr(getattr(mod, 'status'), file), clazz)
            return impl
        except Exception as e:
            raise StatusImplementationError(f"Error Loading StatusImpl: '{fpath}'\n {str(e)}")
