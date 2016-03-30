# ab_searching

## Define connection:

```python
ELASTICSEARCH_HOSTS = 'localhost'
ELASTICSEARCH_PORT = 9200

try:
    from elasticsearch_dsl.connections import connections
    connections.create_connection(hosts=ELASTICSEARCH_HOSTS, port=ELASTICSEARCH_PORT, timeout=20)
except:
    print('Elasticsearch is not in touch')
```

## Example Search index
```python
from searching import indexes
from searching import fields


class ExampleSimpleIndex(indexes.ModelIndex):
    title = fields.CharField(attr='custom_method')

    class Meta(indexes.ModelIndex.Meta):
        model = Example
        fields = ('id', 'slug', 'title',)


class Example2Index(indexes.ModelIndex):
    example = fields.ForeignIndex(ExampleSimpleIndex, null=True)
    pks = fields.ListFields(attr='get_pks', null=True)

    class Meta(indexes.ModelIndex.Meta):
        model = Example2
        fields = ('id', 'slug', 'title', 'example', 'pks')
        index = 'foo'
```
            
## Example Model setup:
```python
from searching.managers import ElasticSearchManager
from searching.mixins import ElasticSearchIndexed


class Example(ElasticSearchIndexed, models.Model):
    slug = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)

    objects = models.Manager()
    search_objects = ElasticSearchManager()

    @classmethod
    def get_model_index(cls):
        from example.search_indexes import ExampleIndex
        return ExampleIndex
```

## Commands:

#### Manual reindex all models:

    ./manage.py manual_indexing_new
    
#### Manual clean index:
 
    ./manage.py clear_index
    
    
For filtering and querying you have to use elasticsearch-dsl way.



## Some settings:

`INDEXING_DEBUG_INFO = True`  - logging info enable or False to disable. (Default: False)

`POST_SAVE_INDEXING = True` - enable index model after save. (Default: True)

 
