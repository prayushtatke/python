import pymongo

class Docdb:
    docdb_client = None
    docdb_conn_str = None
    docdb_database = None
    db = None
    is_mocked = False

    def __init__(self, docdb_conn_str=None, docdb_database=None, mock_client=None):
        self.docdb_conn_str = docdb_conn_str
        self.docdb_database = docdb_database
        if mock_client:
            self.docdb_client = mock_client
            self.is_mocked = True

    @classmethod
    def get_client(cls, docdb_conn_str=None):
        return pymongo.MongoClient(docdb_conn_str)

    def init(self):
        if not self.is_mocked:
            self.docdb_client = Docdb.get_client(self.docdb_conn_str)

        self.db = self.docdb_client.get_database(self.docdb_database)

    def find(self, collection, query, proj):
        coll = self.db.get_collection(collection)
        return coll.find(query, proj)

    def find_one(self,collection,query, proj):
        coll = self.db.get_collection(collection)
        return coll.find_one(query, proj)

    def aggregate(self, collection, pipeline):
        coll = self.db.get_collection(collection)
        return coll.aggregate(pipeline)

    def insrt_doc(self,collection, doc):
        coll = self.db.get_collection(collection)
        return coll.insert_one(doc)

    def insrt_docs(self, collection, docs_list):
        coll = self.db.get_collection(collection)
        return coll.insert_many(docs_list)

    def update_doc(self, collection, filter_query, set_query):
        coll = self.db.get_collection(collection)
        return coll.update_one(filter_query, {'$set': set_query}, upsert=True)

    def close(self):
        self.docdb_client.close()
