from contextlib import suppress

# General Purpose Functions
def is_not_empty(var):
    """
    This is utility method, takes parameter of any type.
    check the exitence of a value.
    e.g. Tests:
        self.assertFalse(util.is_not_empty(None))
        self.assertFalse(util.is_not_empty(''))
        self.assertFalse(util.is_not_empty(' '))
        self.assertFalse(util.is_not_empty({}))
        self.assertFalse(util.is_not_empty([]))

        self.assertTrue(util.is_not_empty(False))
        self.assertTrue(util.is_not_empty(' A '))
        self.assertTrue(util.is_not_empty([1]))
        self.assertTrue(util.is_not_empty({"key" : None}))
        self.assertTrue(util.is_not_empty(1))
        self.assertTrue(util.is_not_empty(1.000))
        self.assertTrue(util.is_not_empty(0))
        self.assertTrue(util.is_not_empty(0.0))
    :param var:
    :return: bool
    """
    if var is None:
        return False

    if var == 0 or False:
        return True

    if var:
        return True if str(var).strip() else False

    return False


def is_empty(var):
    """
        This is utility method, takes parameter of any type.
        check the NON exitence of a value.
        e.g. Tests:
        self.assertTrue(util.is_empty(None))
        self.assertTrue(util.is_empty(''))
        self.assertTrue(util.is_empty('    '))
        self.assertTrue(util.is_empty({}))
        self.assertTrue(util.is_empty([]))

        self.assertFalse(util.is_empty(False))
        self.assertFalse(util.is_empty(' A '))
        self.assertFalse(util.is_empty([1]))
        self.assertFalse(util.is_empty({"key" : None}))
        self.assertFalse(util.is_empty(1))
        self.assertFalse(util.is_empty(1.000))
        self.assertFalse(util.is_empty(0))
        self.assertFalse(util.is_empty(0.0))

        :param var:
        :return: bool
    """
    return not is_not_empty(var)


def find_missing_or_empty_keys(input_coll, key_set):
    """
        Returns the list of missing keys in input collection.
        This is particularly helpful when we have to check multiple
        keys in a collection. it can simplifies the if condition.

        e.g. Usage.

        missing_keys = find_missing_or_empty_keys(payload, [C_NAME, C_ASSET_ID, AGG_WINDOW, SIGNALS])
        if missing_keys:
            log.error(
                f'Missing required fields[{str(missing_keys)}] in the input, input_payload: {str(payload)}')
            raise MissingRequiredInput(f'Missing Required fields[{str(missing_keys)}].')

    :param input_coll:
    :param key_set: keys to search
    :return:
    """
    if (not input_coll) or (not key_set):
        return None

    return list(filter(lambda e: e not in input_coll or is_empty(input_coll[e]), key_set))


def del_dict_keys(input_dict, keys_to_del):
    assert is_not_empty(input_dict) and isinstance(input_dict, dict), \
        "'input_dict' cannot be empty, and should be type of 'dict'"

    with suppress(KeyError):
        for k in keys_to_del:
            del input_dict[k]

