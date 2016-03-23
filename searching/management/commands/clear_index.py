from django.core.management.base import BaseCommand
from elasticsearch_dsl import Index


class Command(BaseCommand):
    help = 'Clean elasticsearch index'

    def handle(self, *args, **options):
        from searching.utils import autodiscover
        for _class in autodiscover():
            index = Index(_class.get_model_index().Meta.index)
            index.delete()
