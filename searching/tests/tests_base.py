import unittest
from elasticsearch_dsl import DocType
from searching.mixins import ElasticSearchIndexed
from .classes import DocTypeClassFactory
from catalog.models import AvtoCatalog


class DocTypeFactoryTests(unittest.TestCase):

    def setUp(self):
        self.factory = DocTypeClassFactory(name='FooClass', index='fooclass', fields=[])

    def test__doctype_name(self):
        self.assertEqual(self.factory._doctype_name, 'FooClassDocType')

    def test_prepare_kwargs(self):
        kwargs = self.factory.prepare_kwargs()
        self.assertIsInstance(kwargs, dict)
        self.assertIsInstance(kwargs['Meta'], type)

    def test_create(self):
        instance = self.factory.create()
        self.assertTrue(issubclass(instance, DocType))


class ElasticSearchIndexed(unittest.TestCase):

    def setUp(self):
        self.instance = AvtoCatalog()

    def test_get_index_name(self):
        self.assertEqual(self.instance._index_name, 'avtocatalog')
        self.assertEqual(self.instance._get_index_name(), 'avtocatalog')
        self.assertEqual(self.instance.doctype_class().__name__,  'AvtoCatalogDocType')
