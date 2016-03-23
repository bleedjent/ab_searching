from .signals import update_to_elastic


class ElasticSearchIndexed(object):

    def save(self, *args, **kwargs):
        super(ElasticSearchIndexed, self).save(*args, **kwargs)
        self.sync_to_elastic()

    @classmethod
    def get_model_index(cls):
        raise NotImplementedError

    def sync_to_elastic(self):
        if self.get_model_index().get_models().filter(pk=self.pk).exists():
            update_to_elastic(self.__class__, self)

    def elastic_serialize(self):
        if hasattr(self, 'get_model_index'):
            return self.get_model_index()(self).serialize()
        return {}

