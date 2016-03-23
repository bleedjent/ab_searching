from elasticsearch_dsl import DocType
from .utils import fields_to_mapping
from .fields import get_from_django_field

META_CLASS_NAME = 'ElasticMeta'


class DocTypeClassFactory(object):

    def __init__(self, model_index):
        self._model_index = model_index
        self._meta = self._model_index.Meta
        self._name = self._meta.model.__name__

    @property
    def _doctype_name(self):
        return '{0}DocType'.format(self._name)

    def prepare_kwargs(self):
        _kwargs = dict(Meta=type('Meta', (), {'index': self._meta.index}))
        _kwargs.update(fields_to_mapping(self._model_index))
        return _kwargs

    def create(self):
        return type(self._doctype_name, (DocType,), self.prepare_kwargs())


class ModelIndex(object):

    class Meta:
        model = None
        fields = []
        exclude = []
        index = 'default'

    def __init__(self, instance=None):
        self.instance = instance
        self._fields = self._get_fields()

    def _get_fields(self):
        result = []
        _fields = self.Meta.fields
        if not _fields:  # if not Meta.fields get all model fields
            _fields = [f.name for f in self.Meta.model._meta.fields]
        for attr_name in _fields:
            if attr_name in self.Meta.exclude:
                continue
            if hasattr(self, attr_name):
                f = getattr(self, attr_name)
            else:
                f = get_from_django_field(self.Meta.model._meta.get_field(attr_name))
            if f:
                f.name = attr_name
                result.append(f)
        return result

    @classmethod
    def get_models(cls):
        return cls.Meta.model.objects.all()

    def serialize(self):
        """
        Method return django instance to dict
        :param instance:
        :return: json(dict)
        """
        _json = {}
        for f in self._fields:
            _json[f.name] = f.serialize(self.instance)
        return _json

    @classmethod
    def _get_doctype_class(cls):
        if not hasattr(cls, '_doctype_class'):
            _factory = DocTypeClassFactory(cls)
            cls._doctype_class = _factory.create()
            cls._doctype_class.init()
        return cls._doctype_class

    doctype_class = _get_doctype_class
