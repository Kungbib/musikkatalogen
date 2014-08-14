# -*- coding: utf-8 -*-
from django.db import models

class Catalog(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_alpha = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u"Katalog"
        verbose_name_plural = u"Kataloger"



class Signum(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    slug = models.SlugField(max_length=50, unique=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u"Signum"
        verbose_name_plural = u"Signum"



class Box(models.Model):
    folder_name = models.CharField(max_length=255, unique=True, verbose_name="Katalognamn", help_text="Filkatalog på disk där denna lådas filer ligger")
    sequence_number = models.IntegerField(db_index=True)
    slug = models.SlugField(max_length=50, unique=True)
    #from_text = models.CharField(max_length=255,db_index=True)
    #to_text = models.CharField(max_length=255,db_index=True)
    label = models.CharField(max_length=255,db_index=True, verbose_name="Etikett")
    catalog = models.ForeignKey(Catalog, related_name="boxes", verbose_name="Tillhör katalog")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s %s' % (self.sequence_number, self.label)

    class Meta:
        verbose_name = u"Låda"
        verbose_name_plural = u"Lådor"
        ordering = ['sequence_number']



class Card(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name="Kortnamn", help_text="Rubriken som visas överst på en kortsida")
    filename = models.CharField(max_length=255, db_index=True, verbose_name="Filnamn", help_text="Filnamnet för bildfilen")
    ocr_text = models.TextField(blank=True, help_text="Automatiskt OCR-tolkad text från kortet.")
    letter = models.CharField(max_length=1, null=True, blank=True, db_index=True, verbose_name="Indexbokstav" , help_text="Anges för första kortet för att dela upp katalogen alfabetiskt.")
    sequence_number = models.IntegerField(db_index=True, verbose_name="Sekvensnummer i låda")
    catalog_sequence_number = models.IntegerField(null=True, blank=True, verbose_name="Kortnummer", help_text="Globalt katalognummer som anger kortets plats i katalogen. Används även som identifierare.")
    box = models.ForeignKey(Box, related_name="cards", verbose_name="Låda")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    signum = models.ForeignKey(Signum, related_name="cards", null=True, blank=True, verbose_name="Signum (ej i bruk än)")


    # Fields with manual transcription data
    name_tr = models.CharField(max_length=255, db_index=True, blank=True, null=True, verbose_name="Namn (tranksriberat)", help_text="Transkriberat namn")
    arr_tr = models.CharField(max_length=255, db_index=True, blank=True, null=True, verbose_name="Arrangemang av", help_text="Transkriberad information om arrangemangets upphovsmän")
    pseudonym_tr = models.CharField(max_length=255, db_index=True, blank=True, null=True, verbose_name="Pseudonym", help_text="Transkriberad pseudonym")
    title_tr = models.CharField(max_length=255, db_index=True, blank=True, null=True, verbose_name="Verkets namn", help_text="Transkriberad version av verkets namn")
    comment = models.TextField(blank=True, null=True, verbose_name="Intern kommentar", help_text="Visas ej för besökare.")

    # readonly field to show preview pic in django admin interface
    def image_tag(self):
        return u'<img alt="Kort %s" src="/static/alfa/%s" />' % (self.catalog_sequence_number, self.box.folder_name + "/" + self.filename.replace(".jpg", "_view500.jpg"))
    image_tag.short_description = 'Bild'
    image_tag.allow_tags = True

    def __unicode__(self):
        return u'%s %s' % (self.catalog_sequence_number, self.name)

    class Meta:
        verbose_name = u"Kort"
        verbose_name_plural = u"Kort"
        ordering = ['catalog_sequence_number']
