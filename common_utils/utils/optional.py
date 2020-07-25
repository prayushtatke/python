from common_utils.utils.commons import is_empty, is_not_empty

class OptionalNoneValueError(Exception):
    pass

class Optional:
    def __init__(self, value=None ):
        self._value = value

    @staticmethod
    def empty():
        return Optional(None)

    def is_present(self) -> bool:
        return is_not_empty(self._value)

    def get(self):
        if not self.is_present():
            raise OptionalNoneValueError('Called get on empty optional')

        return self._value

    def get_or_else(self, default: object):
        try:
            return self.get()
        except OptionalNoneValueError:
            return default

    def get_or_raise(self, exception, *args, **kwargs):
        if is_empty(self._value):
            raise exception(*args, **kwargs)
        else:
            return self._value


    def __str__(self):
        if is_empty(self._value):
            return 'Optional empty'
        else:
            return 'Optional of: {}'.format(self._value)

    def __repr__(self):
        return 'Optional({})'.format(repr(self._value))

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Optional) and o._value == self._value

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)
