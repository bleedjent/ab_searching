ab_searching

Define connection

    ELASTICSEARCH_HOSTS = 'localhost'
    ELASTICSEARCH_PORT = 9200

    try:
        from elasticsearch_dsl.connections import connections
        connections.create_connection(hosts=ELASTICSEARCH_HOSTS, port=ELASTICSEARCH_PORT, timeout=20)
    except:
        print('Elasticsearch is not in touch')


Example Search index

    from searching import indexes
    from searching import fields


    class ExampleSimpleIndex(indexes.ModelIndex):
        title = fields.CharField(attr='custom_method')

        class Meta(ModelIndex.Meta):
            model = Example
            fields = ('id', 'slug', 'title',)


    class Example2Index(indexes.ModelIndex):
        example = fields.ForeignIndex(ExampleSimpleIndex, null=True)
        pks = fields.ListFields(attr='get_pks', null=True)

        class Meta(AvtoCatalogSimpleIndex.Meta):
            model = Example2
            fields = ('id', 'slug', 'title', 'example', 'pks')
            index = 'foo'

