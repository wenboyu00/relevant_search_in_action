from es_client import EsClient
from read_source_data import get_companies_info


class CompanySearch:
    def __init__(self, host):
        self.es = EsClient([host])

    def get_index_mapping(self):
        mapping = {
            "mappings": {
                "_doc": {
                    "properties": {
                        "name": {"type": "text"},
                        "code": {"type": "keyword"},
                        "registrationDay": {"type": "date"},
                        "character": {"type": "keyword"},
                        "legalRepresentative": {"type": "text"},
                        "capital": {"type": "text"},
                        "businessScope": {"type": "text"},
                        "province": {"type": "keyword"},
                        "city": {"type": "text"},
                        "address": {"type": "text"},
                    }
                }
            }
        }
        return mapping

    def create_company_index(self):
        company_mapping = self.get_index_mapping()
        self.es.creat_index("company", company_mapping)

    def insert_companies_info(self):
        companies_info = get_companies_info()
        self.es.update("company", companies_info, 'code')

    def search_company(self, keyword):
        body = {"query": {"match_all": {}}}
        result = self.es.search("company", body)
        print(result)


if __name__ == '__main__':
    host = {"host": "localhost", "port": 9200}
    cs = CompanySearch(host)
    cs.search_company(keyword="123")
