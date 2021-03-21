import logging

from elasticsearch import Elasticsearch, helpers
from elasticsearch.client import IndicesClient
from elasticsearch.helpers import BulkIndexError

logger = logging.getLogger(__name__)


class EsClient:
    def __init__(self, hosts):
        self.es = Elasticsearch(hosts=hosts)
        self.helpers = helpers

    def creat_index(self, index, body):
        # https://elasticsearch-py.readthedocs.io/en/6.3.0/api.html?highlight=mapping#elasticsearch.client.IndicesClient.put_mapping
        index_client = IndicesClient(self.es)
        result = index_client.create(index=index, body=body)
        return result

    def update(self, index, rows, id_key, doc_type="_doc", update_count=100):
        # https://elasticsearch-py.readthedocs.io/en/6.3.0/helpers.html?highlight=bulk#bulk-helpers
        docs = list()
        for row in rows:
            _id = row[id_key]
            doc = {
                "_id": _id,
                "_type": doc_type,
                "_index": index,
                # doc_as_upsert = True, 没有则创建
                "_source": {'doc': row, 'doc_as_upsert': True},
                '_op_type': 'update'
            }
            docs.append(doc)
            print(doc)
            if len(docs) >= update_count:
                try:
                    self.helpers.bulk(self.es, docs)
                    docs = []
                except BulkIndexError as e:
                    logger.warning(e.errors)
                    docs = []

        result = self.helpers.bulk(self.es, docs)
        return result

    def search(self, index, body):
        return self.es.search(index=index, body=body)



