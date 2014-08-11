# -*- coding: utf-8 -*-
from django.contrib import admin
from cards.models import *


class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'box_name', 'order', 'catalog_sequence_number', 'filename', 'ocr_text', 'letter', 'updated_at')
    search_fields = ['name', 'ocr_text']

    def order(self, instance):
        return str(instance.box.slug) + "-" + str(instance.sequence_number)

    def box_name(self, instance):
        return instance.box.folder_name


class BoxAdmin(admin.ModelAdmin):
    list_display = ('slug', 'folder_name', 'catalog_name', 'sequence_number', 'label', 'updated_at')

    def catalog_name(self, instance):
        return instance.catalog.name


class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Card, CardAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(Catalog, CatalogAdmin)
