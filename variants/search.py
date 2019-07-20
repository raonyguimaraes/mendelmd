from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection(hosts=['es01:9200'])


class VariantIndex(DocType):
    pos_index = Text()
    chr = Text()
    pos = Text()
    variant_id = Text()
    ref = Text()
    alt = Text()

    class Meta:
        index = 'variant-index'


def bulk_indexing():
    VariantIndex.init('variant-indexing')
    es = Elasticsearch(hosts=[{'host': 'es01', 'port': 9200}])
    bulk(client=es, actions=(b.indexing() for b in models.Variant.objects.all().iterator()))
