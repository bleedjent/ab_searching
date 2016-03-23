from distutils.core import setup

setup(
        name='ab_searching',
        version='0.1.0',
        packages=['searching', 'searching.tests', 'searching.management', 'searching.management.commands'],
        url='',
        license='',
        author='Dr.bleedjent',
        author_email='dr.bleedjent',
        description='AvtoBazar Searching Tools based on elasticsearch-dsl',
        install_requires=[
            'elasticsearch-dsl>=2.0.0,<3.0.0',
            'django>=1.7.3',
        ]
)
