import logging
from .settings import POST_SAVE_INDEXING, INDEXING_DEBUG_INFO

logger = logging.getLogger(__name__)


def update_to_elastic(sender, instance, **kwargs):
    if POST_SAVE_INDEXING:
        doctype = instance.get_model_index().doctype_class()
        document = doctype(**instance.elastic_serialize())
        document.meta.id = instance.pk
        document.save()
        if INDEXING_DEBUG_INFO:
            logger.info('{0} sended to index {1}'.format(str(instance), document.meta.index))
