# Common Utils for Python applications

## 'get_logger()' function.
creates a logger.
`def get_logger(logger_name, log_level='DEBUG', log_format='%(asctime)s:%(levelname)s: %(message)s'):`

Usage:

	>>> logger = get_logger(__name__) # to use application name OR
	>>> logger = get_logger('AppName') # specific name
	>>> logger = get_logger('AppName', log_level=INFO) # starts with log levels as INFO
	>>> logger = get_logger('AppName', log_level='INFO', log_format='<>') # with specific format.
	 

## Decorators:
	- log_exception
	- raise_exception

**log_exception**:

``def log_exception(logger=None, err_msg='', catch=Exception):``

*Note:*
In all below examples, application logger can also be provided as shown above.

Usage:
- to add simple try-except block
 
   @log_exception()
   def foo(**args, **kwargs):
   // code


 is equivalent to:

	def foo(**args, **kwargs):
      try:
          // code
      except Exception as e:
          log.exception(str(e))
              
- catch a specific exception and log it with specific msg.

	@log_exception(catch=KeyError, err_msg='No Key Found')
    def foo(**args, **kwargs):
      // code
 
 
is equivalent to:
    
    def foo(**args, **kwargs):
       try:
          // code
       except KeyError as e:
          # logging original err msg.
          log.error(str(e)) 
          log.exception('No Key Found')
           	
 - catch multiple exceptions and log it with specific msg.


    @log_exception(catch=(DBError,ConnectionError), err_msg='Some Error')
    def foo(**args, **kwargs):
        // code
  
is equivalent to:
    
    def foo(**args, **kwargs):
       try:
          // code
       except (DBError,ConnectionError) as e:
          # logging original err msg.
          log.error(str(e)) 
          log.exception('Some Error')
 

**raise_exception**:

`def raise_exception(logger=None, err_msg='', catch=Exception, throw=None):`

*Note:*
In all below examples, application logger can also be provided as shown above.

Usage:
 - to add simple try-except and raise block
 
 
	@raise_exception()
	def foo(**args, **kwargs):
	   // code
	
is equivalent to:

	def foo(**args, **kwargs):
      try:
          // code
      except Exception as e:
          log.error(str(e))
          raise
              
 - catch a specific exception and raise another with specific msg.


    @raise_exception(catch=KeyError, throw=RuntimeError, err_msg='Some Error')
    def foo(**args, **kwargs):
        // code
  
 is equivalent to:
    
    def foo(**args, **kwargs):
       try:
          // code
       except KeyError as e:
          # logging original err msg.
          log.error(str(e)) 
          raise RuntimeError(Some Error)
           	
 - catch multiple exceptions and and raise another with specific msg.

 
    @raise_exception(catch=(DBError,ConnectionError), throw=EnvironmentError, err_msg='Some Environment Error')
    def foo(**args, **kwargs):
        // code
  
 is equivalent to:
    
    def foo(**args, **kwargs):
       try:
          // code
       except (DBError,ConnectionError) as e:
          # logging original err msg.
          log.error(str(e)) 
          raise EnvironmentError('Some Environment Error')
---
## redis_util.py
This module contains helper class 'Redis' to perform usual get/set keys from Redis.
This module eases the client application to query Redis, as client doesn't need to 
convert the stored into python objects.

Usages:

- To initialize a connection and store and get a key in namespace.

        from utils.redis_util import Redis
        // provide host, port , password directly.
        // namespace is optional, if providedwill be taken as default namespace for further operation.
        // although all the methods have namespace parameter to override the default.
    
          redis = Redis(host='localhost', port=6379, password=*****, namespace='test')
         
        // OR To get host ,port, password info from AWS paramstore, just pass 'aws_param_name'
          redis = Redis(aws_param_name=<param_name>)
         
        // OR to get redis password from AWS secret. just pass __host__, (port is 6379 by default) 'aws_secret_name' and (optional) 
        // 'aws_secret_pass_key' ('redis_pass' is taken as default).
          redis = Redis(host=host, aws_secret_name=<secret_name>, aws_secret_pass_key='redis_password')
             
- To store and retrieve key from redis.
  Note: all _get_ methods returns an _Optional_ object(https://pypi.org/project/pyOptional/).
        So client have to check for the availability for a value(by calling get()).
        
        # Storing by _.set_hkey()_, and retrievng by _.get_hkey('key_str')_
        redis.set_hkey('key_str', 'value')
        value = redis.get_hkey('key_str')
        self.assertTrue(value.is_present())
        self.assertEqual(value.get(), 'value')
        
- To Store and retrieve different DataTypes.

        # single string as key, and string as value
        redis.set_hkey('key_int', 1)
        value = redis.get_hkey('key_int')

        self.assertEqual(value.get(), 1)

        # single string as key, and string as value
        redis.set_hkey('key_float', 1.5)
        value = redis.get_hkey('key_float')
        self.assertEqual(value.get(), 1.5)

        value = redis.get_hkey('a_non_existent_key')
        self.assertFalse(value.is_present())
        
        # multiple string to join as key, and stringified dict as value
        dict_val = {'k1': 'v1', 'k2':'v2'}
        redis.set_hkey(['k1', 'k2'], str(dict_val).encode('utf-8'))
        value = redis.get_hkey(['k1', 'k2'])
        self.assertDictEqual(value.get(), dict_val)

        # storing big dict having multiple types of values
        dict_val = {'k1': 'v1', 'k2': 1, 'k3': 2.5, 'k4': {'k4_1': 'v4_1', 'k4_2': 'v4_2'}}
        redis.set_hkey('key_dict', str(dict_val).encode('utf-8'))
        value = redis.get_hkey('key_dict')
        self.assertDictEqual(value.get(), dict_val)

        # storing big dict having multiple types of values as JSON
        redis.set_hkey('key_dict_json', json.dumps(dict_val).encode('utf-8'))
        value = redis.get_hkey('key_dict_json')
        self.assertDictEqual(value.get(), dict_val)

        # storing list
        list_val = ['one', 'two']
        redis.set_hkey('key_list', str(list_val).encode('utf-8'))
        value = redis.get_hkey('key_list')
        self.assertListEqual(value.get(), list_val)

        # storing set
        set_val = set(['one', 'two'])
        redis.set_hkey('key_set', str(set_val).encode('utf-8'))
        value = redis.get_hkey('key_set')
        self.assertSetEqual(value.get(), set_val)        
 
 - To retrieve all keys of namespace
        
        # single string as key, and string as value
        hm = { 'key:str:w123': 'v1', 'key:int': 1, 'key:float': 1.5}
        redis.set_hm(hm)
        
        result = redis.getall_hkeys()
        self.assertDictEqual(hm, result.get())
 
 - To retrieve  all keys with pattern from namespace:
 
         # single string as key, and string as value
        hm = {
                'key_111:abc:111': 'v1',
                'key_111:def:222': 'v2',
                'key_222:abc:333': 'v3',
                'key_222:ghi:111': 'v4'
            }
        redis.set_hm(hm)

        keys_prefix = redis.getall_hkeys(key_prefix='key_111')
        self.assertTrue(keys_prefix.is_present())
        keys_prefix = keys_prefix.get()
        self.assertEqual(len(keys_prefix), 2)
        self.assertEqual(keys_prefix['key_111:abc:111'], 'v1')
        self.assertEqual(keys_prefix['key_111:def:222'], 'v2')

        keys_suffix = redis.getall_hkeys(key_suffix='111')
        self.assertTrue(keys_suffix.is_present())
        keys_suffix = keys_suffix.get()
        self.assertEqual(len(keys_suffix), 2)
        self.assertEqual(keys_suffix['key_111:abc:111'], 'v1')
        self.assertEqual(keys_suffix['key_222:ghi:111'], 'v4')

        keys_contains = redis.getall_hkeys(key_contains='abc')
        self.assertTrue(keys_contains.is_present())
        keys_contains = keys_contains.get()
        self.assertEqual(len(keys_contains), 2)
        self.assertEqual(keys_contains['key_111:abc:111'], 'v1')
        self.assertEqual(keys_contains['key_222:abc:333'], 'v3')  