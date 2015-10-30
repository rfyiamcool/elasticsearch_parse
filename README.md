#elasticsearch_parse
=================

首先注明下本项目是由来,学习Elasticsearch本身是有些痛苦的, 我们可以熟练的编写SQL 、 Mongodb语句，但对于Elasticsearch Dsl语法总是蒙头，一个劲的翻找笔记...  
简单说 Elasticsearch Parse可以让你更容易的上手ES, 他的功能主要是语句映射, 有点ORM的意思... 

此项目继承于`elasticsearch-dsl-py`, 其实砍掉了大量的代码,然后中间又加了一些佐料, 只是为了DSL语句映射功能 ! 

用原始的DSL语法操作的过程  
```
from elasticsearch import Elasticsearch
client = Elasticsearch()

response = client.search(
    index="my-index",
    body={
      "query": {
        "filtered": {
          "query": {
            "bool": {
              "must": [{"match": {"title": "python"}}],
              "must_not": [{"match": {"description": "beta"}}]
            }
          },
          "filter": {"term": {"category": "search"}}
        }
      },
      "aggs" : {
        "per_tag": {
          "terms": {"field": "tags"},
          "aggs": {
            "max_lines": {"max": {"field": "lines"}}
          }
        }
      }
    }
)

```

下面是使用Elasticsearch_parse的用法

```
from elasticsearch_parse import Search, Q

s = Search(using=client, index="my-index") \
    .filter("term", category="search") \
    .query("match", title="python")   \
    .query(~Q("match", description="beta"))

s.aggs.bucket('per_tag', 'terms', field='tags') \
    .metric('max_lines', 'max', field='lines')

response = s.execute()
```
