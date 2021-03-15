#《相关性搜索：利用solr与ElasticSearch创建智能应用》的实践

目标：根据书中的方法，完善搜索，并尽力提高搜索相关性。

使用ElasticSearch版本：6.8.x
使用elasticsearch-py，是官方低层级封装py包

github地址：https://github.com/elastic/elasticsearch-py

文档地址：https://elasticsearch-py.readthedocs.io/en/6.8.2/index.html

使用数据：Enterprise-Registration-Data

中文分词器：https://github.com/medcl/elasticsearch-analysis-ik

# 设计以相关性为核心的搜索
三个步骤：收集信息和需求，设计搜索应用，部署监控改进

## 信息和需求的收集
三个步骤：找出用户要问的问题，找出商业需求，找出必要及可用的信息
### 理解用户的需求
设计几个角色代表来代表不同的用户类型，找出不同类型用户的典型需求，设计时避免行为重叠。
- 普通用户：通过人名或者公司部分名字来查找公司信息
- 市场销售：关注某地区，某行业，某时间段的公司。也有时需要通过注册码来找到某个公司

理解业务需求，可能有一些公司像排在前排

需求结论：
   - 公司名称搜索
   - 法人名称搜索
   - 注册时间区间筛选
   - 经营类型搜索匹配
   - 城市和省会搜索
## 设计搜索应用
两个目标：1功能，2体验
### 定义字段和模型的信号
对字段定义需要通过迭代的方式完成。
以分类的方式来思考字段，可以简化迭代过程。
书中把示例的字段分为：位置，偏好，内容和业务。这个实践只需要考虑：位置，时间和内容。

| 字段名              | 信息         | 分析              |
| ------------------- | ------------ | ----------------- |
| name                | 公司名，全称 | ik_max_word分词 |
| code                | 代码         | 不分词            |
| registrationDay     | 注册时间     | date格式          |
| legalRepresentative | 法人代表     | ik_max_word分词   |
| businessScope       | 经营范围     | ik_max_word分词   |
| province            | 省份         | 不分词            |
| city                | 城市         | 不分词            |
| address             | 地址         | ik_max_word分词   |

