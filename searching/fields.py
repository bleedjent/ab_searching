from elasticsearch_dsl import String, Nested, Date, Boolean


def get_from_django_field(field):
    _field_class = FIELD_MAP.get(field.__class__.__name__, BaseField)
    return _field_class()


class BaseField(object):
    mapping_class = String

    def __init__(self, name=None, attr=None, null=True, **kwargs):
        self.name = name
        self.attr = attr
        self.null = null

    def serialize(self, instance):
        value = getattr(instance, self.name, None)
        if value is None and self.attr is not None:
            value = getattr(instance, self.attr, None)
        if value and hasattr(value, '__call__'):
            value = value()
        if not value and not self.null:
            raise 'Field {0} Not allowed null values'.format(self.name)
        return value

    def to_mapping(self):
        return self.mapping_class()


class DateField(BaseField):
    mapping_class = Date


class ForeignIndex(BaseField):
    mapping_class = Nested

    def __init__(self, model_index, **kwargs):
        self.model_index = model_index
        super(ForeignIndex, self).__init__(**kwargs)

    def serialize(self, instance):
        value = super(ForeignIndex, self).serialize(instance)
        if value:
            value = self.model_index(value).serialize()
            return value or []
        return []

    def to_mapping(self):
        from .utils import fields_to_mapping
        return self.mapping_class(properties=fields_to_mapping(self.model_index))


class ManyIndex(ForeignIndex):

    def serialize(self, instance):
        value = []
        for item in list(getattr(instance, self.name).all()):
            _val = self.model_index(item).serialize()
            if _val:
                value.append(_val)
        return value


class CharField(BaseField):
    pass


class ListFields(BaseField):

    def to_mapping(self):
        return self.mapping_class(fields={'raw': String(index='not_analyzed')})

    def serialize(self, instance):
        value = super(ListFields, self).serialize(instance)
        if isinstance(value, list):
            return value
        raise '`{0}` ListField.serialize must return list'.format(self.name)


class ListQuerysetFields(ListFields):

    def serialize(self, instance):
        return list(getattr(instance, self.name).values_list(self.attr, flat=True))


class BooleanField(BaseField):
    mapping_class = Boolean

    def serialize(self, instance):
        return bool(super(BooleanField, self).serialize(instance))


FIELD_MAP = {
    # 'OneToOneField': ForeignIndex,
    'DateTimeField': DateField,
    'DateField': DateField,
    'BooleanField': BooleanField
}