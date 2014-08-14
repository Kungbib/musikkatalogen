# -*- coding: utf-8 -*-
from django.db import models

class Catalog(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_alpha = models.BooleanField(default=False)


    class Meta:
        verbose_name = u"Katalog"
        verbose_name_plural = u"Kataloger"



class Signum(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = u"Signum"
        verbose_name_plural = u"Signum"



class Box(models.Model):
    folder_name = models.CharField(max_length=255, unique=True)
    sequence_number = models.IntegerField(db_index=True)
    slug = models.SlugField(max_length=50, unique=True)
    #from_text = models.CharField(max_length=255,db_index=True)
    #to_text = models.CharField(max_length=255,db_index=True)
    label = models.CharField(max_length=255,db_index=True)
    catalog = models.ForeignKey(Catalog, related_name="boxes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"Låda"
        verbose_name_plural = u"Lådor"
        ordering = ['sequence_number']



class Card(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    filename = models.CharField(max_length=255, db_index=True)
    ocr_text = models.TextField(blank=True)
    letter = models.CharField(max_length=1, null=True, blank=True, db_index=True)
    sequence_number = models.IntegerField(db_index=True)
    catalog_sequence_number = models.IntegerField(null=True, blank=True)
    box = models.ForeignKey(Box, related_name="cards")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    signum = models.ForeignKey(Signum, related_name="cards", null=True, blank=True)

    # Fields with manual transcription data
    name_tr = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    arr_tr = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    pseudonym_tr = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    title_tr = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    # readonly field to show preview pic in django admin interface
    def image_tag(self):
        return u'<img alt="Kort %s" src="/static/alfa/%s" />' % (self.name, self.box.folder_name + "/" + self.filename.replace(".jpg", "_view500.jpg"))
    image_tag.short_description = 'Bild'
    image_tag.allow_tags = True

    class Meta:
        verbose_name = u"Kort"
        verbose_name_plural = u"Kort"
        ordering = ['catalog_sequence_number']
