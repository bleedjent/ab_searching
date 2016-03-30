from elasticsearch_dsl import String, Nested, Date, Boolean, Integer, Object


def get_from_django_field(field):
    _field_class = FIELD_MAP.get(field.__class__.__name__, BaseField)
    return _field_class()


class BaseField(object):
    """
    Every field must inherit this class. Should be abstract.
    """

    def __init__(self, name=None, attr=None, null=True, **kwargs):
        self.name = name
        self.attr = attr
        self.null = null

    def serialize(self, instance):
        # Check if index has function for custom serializing and call it, if exists
        handler = getattr(instance, 'prepare_%s' % self.name, None)
        if handler and callable(handler):
            return handler(instance)

        value = getattr(instance, self.name, None)
        if value is None and self.attr is not None:
            value = getattr(instance, self.attr, None)
        if value and callable(value):
            if self.name == 'makes':
                import ipdb; ipdb.set_trace()
            value = value()
        if not value and not self.null:
            raise Exception('Field {0} doesn`t allow null values'.format(self.name))
        return value

    def to_mapping(self):
        return self.mapping_class()


class CharField(BaseField):
    mapping_class = String


class DictField(BaseField):
    mapping_class = Object


class DateTimeField(BaseField):
    mapping_class = Date


class IntegerField(BaseField):
    mapping_class = Integer


class BooleanField(BaseField):
    mapping_class = Boolean

    def serialize(self, instance):
        return bool(super(BooleanField, self).serialize(instance))


class ForeignIndex(BaseField):
    mapping_class = Object

    def __init__(self, model_index, **kwargs):
        self.model_index = model_index
        super(ForeignIndex, self).__init__(**kwargs)

    def serialize(self, instance):
        value = super(ForeignIndex, self).serialize(instance)
        if value:
            value = self.model_index(value).serialize()
            return value or {}
        return {}

    def to_mapping(self):
        from .utils import fields_to_mapping
        return self.mapping_class(properties=fields_to_mapping(self.model_index))


class ListField(BaseField):
    """
    Class for serializing list objects (that doesn`t contains objects).
    For list of objects use ManyIndexField.
    """
    mapping_class = String

    def to_mapping(self):
        return self.mapping_class(fields={'raw': String(index='not_analyzed')})

    def serialize(self, instance, value=None):
        """
        Checks if list if list contains objects, that can be serialized, and serialize it.
        """
        if value is None:
            value = super(ListField, self).serialize(instance)
            if value is None:
                return []

        if hasattr(value, '__iter__'):
            for i, obj in enumerate(value):
                if hasattr(obj, 'get_model_index'):
                    value[i] = obj.get_model_index().serialize()
                elif hasattr(self, 'model_index'):
                    value[i] = self.model_index(obj).serialize()
            return list(value)
        else:
            raise Exception('`{0}` field must be iterable (or return iterable)'.format(self.name))


class ListQuerysetField(ListField):
    """
    Intended for getting specific field from queryset. Use with queryset.
    :params:
        attr - model field name.
        values_list_attr - name of field, that we take from model.
    """
    def __init__(self, values_list_attr, **kwargs):
        self.values_list_attr = values_list_attr
        super(ListQuerysetField, self).__init__(**kwargs)

    def serialize(self, instance):
        queryset = getattr(instance, self.name, None)
        if queryset is None and self.attr is not None:
            queryset = getattr(instance, self.attr, None)
        if queryset.exists():
            return list(queryset.values_list(self.values_list_attr, flat=True))
        return []


class ManyIndexField(ListField):
    """
    This field intended for indexing ManyToMany fields (or list of objects).
    """
    mapping_class = Nested

    def __init__(self, model_index=None, **kwargs):
        self.model_index = model_index
        super(ManyIndexField, self).__init__(**kwargs)

    def serialize(self, instance):
        try:
            queryset = getattr(instance, self.name).all()
            return super(ManyIndexField, self).serialize(instance, queryset)
        except AttributeError:
            raise Exception('`{0}` field must be many to many field'.format(self.name))


FIELD_MAP = {
    'DateTimeField': DateTimeField,
    'DateField': DateTimeField,
    'BooleanField': BooleanField,
}
