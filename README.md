
PYCIPAC
=======

This is a lightweight web application of a Card-Image Public Access Catalog (CIPAC).
It is used to display scanned library catalog cards. It was written in a haste
as a proof of concept and you will probably find numerous bugs.


Installation
------------

Install prerequisites for Django 1.6.5. Create a database in MySql with the correct collation:

> CREATE DATABASE pycipac CHARACTER SET utf8 collate utf8_swedish_ci;


Run table migrations:

$ python manage.py syncdb

(create admin user)


Create a catalog item in the admin GUI.


Import all folders with scanned images and their corresponding OCR files to a specific catalog:

$ python manage.py import <path/to/folder> <catalog_slug>

(repeat for all folders)


Generate global sequence numbers for all cards in the catalog:

$ python manage.py resequence <catalog_slug>


Start server:

$ python manage.py runserver
