from django.db import models
from elasticsearch_dsl.query import Q


class ElasticSearchManager(models.Manager):

    def iterator(self):
        return iter(self.execute())

    def get_queryset(self):
        return self.model.get_model_index().doctype_class().search()

    def filter(self, **kwargs):
        return self.get_queryset().filter(**kwargs)

    def exclude(self, **kwargs):
        return self.get_queryset().exclude(**kwargs)

    def query(self, **kwargs):
        return self.get_queryset().query(**kwargs)

    def multi_match_query(self, **kwargs):
        return self.get_queryset().query(Q("multi_match", **kwargs))
