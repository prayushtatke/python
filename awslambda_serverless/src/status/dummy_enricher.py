from .status import Status

class DummyEnricherImpl(Status):
	__status_code = {'type_1': {'-1': 'c', '0': 'e', '1': 'e', '2': 'e', '3': 'o'},
                     'type_2': {'b': 'e'}
                    }
    __default_status = {'type_1': 'u', 'type_2': 'o'}

    def apply_filter(self, payload):
        pass

    def enrich(payload):
        return {'status' : 'Dummy.' +'.'.join(payload.keys())}

