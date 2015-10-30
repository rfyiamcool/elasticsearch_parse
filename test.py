from elasticsearch_parse import Search, Q


s = Search(index="my-index") \
    .filter("term", blog="xiaorui.cc") \
    .query("match", author="ruifengyun")   \
    .query(~Q("match", face="good"))

s.aggs.bucket('per_tag', 'terms', field='tags')

print s.execute()
