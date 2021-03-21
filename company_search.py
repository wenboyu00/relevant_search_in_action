from copy import deepcopy

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
                        "name": {"type": "text", "analyzer": "ik_max_word"},
                        "code": {"type": "keyword"},
                        "registrationDay": {"type": "date"},
                        "character": {"type": "keyword"},
                        "legalRepresentative": {"type": "text", "analyzer": "ik_max_word"},
                        "capital": {"type": "keyword"},
                        "businessScope": {"type": "text", "analyzer": "ik_max_word"},
                        "province": {"type": "keyword"},
                        "city": {"type": "keyword"},
                        "address": {"type": "text", "analyzer": "ik_max_word"},
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

    def search_company(self, keyword=None, start_date=None, end_date=None, query_filed=None):
        """

        :param keyword: 搜索关键字
            - 搜索字段 ："name^3", "legalRepresentative^3", "businessScope^2", "address"
                - 名字和法人 权重最高，设为3倍权重
                - 经营范围 其次，2倍权重
                - 地址 1倍权重
            - keyword_query：用ik_max_word分词器，匹配出分数相加最高的字段
            - keyword_query_cross_fields：把目标字段作为同一个字段进行匹配
        :param start_date: 注册时间筛选开始时间，大于等于
        :param end_date: 注册时间筛选结束时间，小于等于
        :param query_filed: 搜索后返回字段
        :return:result_list:搜索结果列表
        """
        if query_filed is None:
            query_filed = []
        # 筛选列表
        filter_list = list()
        if start_date and end_date:
            date_range = {"range": {"registrationDay": {"gte": start_date, "lte": end_date}}}
            filter_list.append(date_range)
        # 关键字搜索
        if not keyword:
            keyword_query = {"match_all": {}}
            keyword_query_cross_fields = keyword_query
        else:
            keyword_query = {"multi_match": {
                "fields": ["name^3", "legalRepresentative^3", "businessScope^2", "address"],
                "query": keyword,
                "analyzer": "ik_max_word",
                "type": "most_fields"
            }}
            keyword_query_cross_fields = deepcopy(keyword_query)
            keyword_query_cross_fields["multi_match"]["minimum_should_match"] = "50%"
            keyword_query_cross_fields["multi_match"]["type"] = "cross_fields"
            keyword_query_cross_fields["multi_match"]["operator"] = "and"

        body = {
            "query": {
                "bool": {
                    "should": [keyword_query, keyword_query_cross_fields],
                    "filter": filter_list
                }
            }

        }

        response = self.es.search("company", body)
        result_list = list()
        for hit in response['hits']['hits']:
            result_dict = {
                "index": hit.get('_index', None),
                "score": hit.get('_score', None)
            }
            for k in query_filed:
                result_dict[k] = hit.get('_source').get(k, None)
            result_list.append(result_dict)
        return result_list


if __name__ == '__main__':
    host = {"host": "localhost", "port": 9200}
    cs = CompanySearch(host)
    # cs.create_company_index()
    # cs.insert_companies_info()
    company_need_filed = ["name", "code", "registrationDay", "legalRepresentative", "businessScope",
                          "province", "city", "address"]
    result = cs.search_company(keyword="雅丽", start_date="1999-01-01", end_date="1999-12-31",
                               query_filed=company_need_filed)
    for r in result:
        print(r)
