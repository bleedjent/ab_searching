from django.apps import apps
from searching.fields import get_from_django_field


def autodiscover():
    from searching.mixins import ElasticSearchIndexed
    return [_class for _class in apps.get_models() if issubclass(_class, ElasticSearchIndexed)]


def fields_to_mapping(model_index):
    _meta = model_index.Meta
    _mapping = {}
    _fields = _meta.fields
    if not _fields:
        _fields = [f.name for f in _meta.model._meta.fields]

    for attr_name in _fields:
        if attr_name in _mapping.keys():  # skip already created key
            continue

        if hasattr(model_index, attr_name):  # take field from index
            _mapping[attr_name] = getattr(model_index, attr_name).to_mapping()
        else:
            try:  # take attr from model fields
                _mapping[attr_name] = get_from_django_field(_meta.model._meta.get_field(attr_name)).to_mapping()
            except Exception:
                pass
    return _mapping
