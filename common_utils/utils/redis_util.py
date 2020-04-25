import redis
import ast
from pyOptional import Optional
from  common_utils.utils import commons as util
from common_utils.utils.configstore import ConfigStore

class RedisException(Exception):
  pass

class RedisNoKeyFoundException(Exception):
  pass

class Redis:

    client_type = 'Redis'
    logger = util.get_logger('Redis')

    @classmethod
    def get_client(cls, host=None, port=None, password=None):
        """
            Returns new Redis client.
        :param host:
        :param port:
        :param password:
        :return:
        """
        return redis.Redis(host=host, port=port, password=password, ssl=True)


    def __init__(self, host=None, port=6379, password=None,
                 namespace=None, aws_secret_name=None, aws_secret_pass_key='redis_pass', aws_param_name=None,
                 aws_region='eu-west-1',
                 key_delim=':',
                 test_client=None):
        """
        :param host:
        :param port:
        :param password:
        :param namespace:
        :param aws_secret_name: the secret_name
        :param aws_secret_pass_key: the password key stored secret
        :param aws_region:
        :param aws_param_name: implementation will be added in future if required
        """

        self.namespace = namespace
        self.key_delim = key_delim

        self.logger.info('Connecting to Redis Database')
        self.host, self.port , self.password =  None, None, None

        if all([host, port, password]):
            self.host, self.port , self.password =  host, port, password

        # get configs from aws parameter store
        elif aws_param_name is not None:
            params = ConfigStore.get_config(aws_secret_name, store_type='params')
            self.__validate_params(params, ['redis_host', 'redis_pass'])
            prt = int(params.get('redis_port')) if params.get('redis_port') else port
            self.host, self.port , self.password = params['redis_host'], prt, params['redis_pass']

        # get configs from aws secretsmanager
        elif aws_secret_name is not None:
            params = ConfigStore.get_config(aws_secret_name, store_type='secrets')
            self.__validate_params(params, [aws_secret_pass_key])
            self.host, self.port , self.password = host, port, params[aws_secret_pass_key]

        # used for unit testing
        elif test_client is not None:
            self.client = test_client

        try:
            if not test_client:
                self.client = Redis.get_client(self.host, self.port , self.password)
            self.logger.info('Connection to redis database established')
        except Exception as e:
            self.logger.error(str(e))
            raise RedisException(str(e))

    def __validate_params(self, params, keys):
        missing_keys = util.find_missing_or_empty_keys(params, keys)
        if missing_keys:
            self.logger.error(f'Missing required Params[{str(missing_keys)}] in Secret/Param store')
            raise RedisException(f'Missing Required fields[{str(missing_keys)}].')


    def set_hkey(self, key, value, namespace=None):
        """This is to persis key in hash/namespace."""
        ns = namespace if namespace else self.namespace
        if isinstance(key, list):
            self.client.hset(ns, self.key_delim.join(key), value)
        else:
            self.client.hset(ns, key, value)


    def get_hkey(self, key, namespace=None, eval=True ) -> Optional:
        """
         To retrieve a specific Key from namespace.
         Set eval=False to retrieve the data as is in bytes.
         The default behaviour is to convert it into python objects.
        :param key:
        :param namespace:
        :param eval:
        :return:
        """
        ns = namespace if namespace else self.namespace
        val = None
        if isinstance(key, list):
            opt_val = Optional(self.client.hget(ns, self.key_delim.join(key)))
        else:
            opt_val = Optional(self.client.hget(ns, key))

        if opt_val.is_present():
            val = opt_val.get().decode("utf-8")
            if eval:
                return Optional(self.__do_eval(val))

        return opt_val

    def get_hkeys(self, keys : list, namespace=None, eval=True ) -> Optional:
        """
         To retrieve values of given keys from namespace.
         Set eval=False to retrieve the data as is in bytes.
         The default behaviour is to convert it into python objects.
        :param keys:
        :param namespace:
        :param eval:
        :return: returns a dict key values from redis.
        """
        if not isinstance(keys, list):
            raise TypeError(f"'keys' should be 'list' type.")

        keys = list(map(lambda key: self.key_delim.join(key)
                    if isinstance(key, list) else key, keys))

        ns = namespace if namespace else self.namespace
        opt_val = Optional(self.client.hmget(ns, keys))

        if not opt_val.is_present():
            return Optional.empty()

        keyvals = {}
        for idx, value in enumerate(map(lambda d: d.decode("utf-8"), filter(lambda dd: dd is not None, opt_val.get()))):
            keyvals[keys[idx]] = self.__do_eval(value) if eval else value

        return Optional(keyvals)

    def exist_hkey(self, key, namespace=None) -> bool:
        """Check if key exist in namespace."""
        ns = namespace if namespace else self.namespace
        return self.client.hexists(ns, key)


    def set_hkeys(self, hmap, namespace=None):
        """
            To persist a hashmap in Redis.
        :param hmap:
        :param namespace:
        :return:
        """
        ns = namespace if namespace else self.namespace
        self.client.hmset(ns, hmap)


    def getall_hkeys(self, namespace=None, key_prefix=None, key_suffix=None, key_contains=None) -> Optional:
        """
            Returns all keys under hash/ namespace.
            Use 'key_prefix', 'key_suffix', 'key_contains' to filter specific keys.
        :param namespace:
        :param key_prefix:
        :param key_suffix:
        :param key_contains:
        :return:
        """
        ns = namespace if namespace else self.namespace
        # a non existent namespace or hash returns a empty map, and optional of empty map returns True.
        val = self.client.hgetall(ns)
        if val:
            filter_func = None
            if key_prefix:
                filter_func = lambda key : key.startswith(key_prefix)
            elif key_suffix:
                filter_func = lambda key: key.endswith(key_suffix)
            elif key_contains:
                filter_func = lambda key: key_contains in key

            hm = {}
            for k, v in val.items():
                key,  val = k.decode('utf-8'), self.__do_eval(v.decode('utf-8'))
                if filter_func:
                    if filter_func(key):
                        hm[key] = val
                else:
                    hm[key] = val

            return Optional(hm) if len(hm) > 0 else Optional.empty()
        return Optional.empty()


    def del_hkey(self, key, namespace=None, eval=True ):
        ns = namespace if namespace else self.namespace
        self.client.hdel(namespace, key)


    def close(self):
        self.client.close()

    def __do_eval(self, val):
        try:
            return ast.literal_eval(val)
        except Exception:
            return val
