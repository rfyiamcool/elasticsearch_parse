#elasticsearch_parse
=================

首先注明下本项目是由来,学习Elasticsearch本身是有些痛苦的, 我们可以熟练的编写SQL 、 Mongodb语句，但对于Elasticsearch Dsl语法总是蒙头，一个劲的翻找笔记...  
简单说 Elasticsearch Parse可以让你更容易的上手ES, 他的功能主要是语句映射, 有点ORM的意思... 

此项目继承于`elasticsearch-dsl-py`,本来是想fork子项目,开发好后提交pull request, 但是想到我这语法映射的功能, 对于官方来说不是很稀罕,索性直接砍掉了 70% 代码,然后中间又加了一些佐料, 最终只是为了DSL语句映射功能 ! 

模块安装方法:
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

我们把语法的用法给过一遍.
```
s = search.Search()
```

通过match查询,f字段值为55的数据
```
s.query('match', f=55)
```

时间范围
```
s.query('range', ** {'@timestamp': {'lt': 'now'}})
```

外围的size的控制  
```
s = s.query('match', f=42)
s[3].to_dict() {'query': {'match_all': {}}, 'from': 3, 'size': 1}
```

```
assert s.to_dict(size=10) == {"query": {"match": {'f': 42}}, "size": 10}
```

嵌入内部size控制
```
s = search.Search.from_dict({"size": 5})
assert {
     "query": {"match_all": {}},
     "size": 5
} == s.to_dict()
```

对于aggs的聚合的使用
```
s = s.query('match', f=42)
assert {"query": {"match": {'f': 42}}} == s.to_dict()
assert {"query": {"match": {'f': 42}}, "size": 10} == s.to_dict(size=10)
s.aggs.bucket('per_tag', 'terms', field='f').metric('max_score', 'max', field='score')
d = {
    'aggs': {
        'per_tag': {
            'terms': {'field': 'f'},
            'aggs': {'max_score': {'max': {'field': 'score'}}}
         }
    }
```


...


