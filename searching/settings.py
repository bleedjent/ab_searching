from django.conf import settings

POST_SAVE_INDEXING = getattr(settings, 'POST_SAVE_INDEXING', True)

INDEXING_DEBUG_INFO = getattr(settings, 'INDEXING_DEBUG_INFO', False)