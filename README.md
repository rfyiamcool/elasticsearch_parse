#elasticsearch_parse
=================

首先注明下本项目是由来,学习Elasticsearch本身是有些痛苦的, 我们可以熟练的编写SQL 、 Mongodb语句，但对于Elasticsearch Dsl语法总是蒙头，一个劲的翻找笔记...  
简单说 Elasticsearch Parse可以让你更容易的上手ES, 他的功能主要是语句映射, 有点ORM的意思... 

此项目继承于`elasticsearch-dsl-py`, 其实砍掉了大量的代码,然后中间又加了一些佐料, 只是为了DSL语句映射功能 ! 

安装方法:
```
pip install elasticsearch_parse
```

下面我们来体验下封装后的es语法解释器.

首先用原始的DSL语法操作,一眼望去会有些麻烦, 手写起来会更麻烦.  
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

下面是使用Elasticsearch_parse的用法,要多简单就多简单

```
from elasticsearch_parse import Search, Q

s = Search(index="my-index") \
    .filter("term", blog="xiaorui.cc") \
    .query("match", author="ruifengyun")   \
    .query(~Q("match", face="good"))

s.aggs.bucket('per_tag', 'terms', field='tags')

response = s.execute()
```
我们得到的结果是:
```
{
    "query": {
        "filtered": {
            "filter": {
                "term": {
                    "blog": "xiaorui.cc"
                }
            },
            "query": {
                "bool": {
                    "must_not": [
                        {
                            "match": {
                                "face": "good"
                            }
                        }
                    ],
                    "must": [
                        {
                            "match": {
                                "author": "ruifengyun"
                            }
                        }
                    ]
                }
            }
        }
    },
    "aggs": {
        "per_tag": {
            "terms": {
                "field": "tags"
            }
        }
    }
}
```

s.query('range', ** {'@timestamp': {'lt': 'now'}})
