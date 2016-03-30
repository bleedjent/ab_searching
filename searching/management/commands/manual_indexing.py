"""
Currently not optimized, only for testing.
"""
from django.core.management.base import BaseCommand

SLICE_SIZE = 1000


class Command(BaseCommand):
    help = 'Manual elasticsearch indexing'

    def handle(self, *args, **options):
        from searching.utils import autodiscover
        for _class in autodiscover():
            try:
                queryset = _class.get_model_index().get_models()
            except NotImplementedError:
                self.stdout.write(self.style.ERROR('No index for "%s"' % _class.__name__))
                continue
            self.stdout.write(self.style.NOTICE('Start indexing "{0}" ({1})'.format(_class.__name__, queryset.count())))
            for i in xrange((queryset.count() // SLICE_SIZE) + 1):
                from_index = (i - 1) * SLICE_SIZE if i > 0 else 0
                to_index = i * SLICE_SIZE if i > 0 else SLICE_SIZE
                current_slice = queryset[from_index:to_index]
                for obj in current_slice:
                    obj.sync_to_elaslstic()
                self.stdout.write('%i adverts indexed from "%s"' % (to_index, _class.__name__))
            self.stdout.write(self.style.NOTICE('Successfully indexed "%s"' % _class.__name__))
