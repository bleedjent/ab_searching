from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Manual elasticsearch indexing'

    def handle(self, *args, **options):
        from searching.utils import autodiscover
        for _class in autodiscover():
            queryset = _class.get_model_index().get_models()
            self.stdout.write(self.style.SUCCESS('Start indexing"{0}" ({1})'.format(_class.__name__, queryset.count())))
            for obj in queryset:
                obj.sync_to_elastic()
            self.stdout.write(self.style.SUCCESS('Successfully indexed "%s"' % _class.__name__))