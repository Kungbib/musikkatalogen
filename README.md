
PYCIPAC
=======

This is a lightweight web application of a Card-Image Public Access Catalog (CIPAC).
It is used to display scanned library catalog cards. It was written in a haste
as a proof of concept and you will probably find numerous bugs.


Installation
------------

Install prerequisites for Django 1.6.5. Create a database in MySql with the correct collation:

> CREATE DATABASE pycipac CHARACTER SET utf8 collate utf8_swedish_ci;

Add a Django settings file and modify it with your settings.

Run table migrations:

$ python manage.py syncdb

(create admin user)


Create a catalog item in the admin GUI.


Import all folders with scanned images and their corresponding OCR files to a specific catalog:

$ python manage.py import <path/to/folder> <catalog_slug>

(repeat for all folders)


Generate global sequence numbers for all cards in the catalog:

$ python manage.py resequence <catalog_slug>


Configure Haystack + Elasticsearch (add to settings.py)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'musikkatalogen',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_MAX_RESULTS = 50
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50

Start Elasticsearch


Build search index:

$ python manage.py rebuild_index


Start server:

$ python manage.py runserver
