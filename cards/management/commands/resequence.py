# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from cards.models import *

class Command(BaseCommand):
    help = 'Generera om sekvensnummer for kort i katalog'
    args = '<catalog_slug>'

    def add_arguments(self, parser):
        parser.add_argument('catalog_slug')

    def handle(self, *args, **options):

        catalog_slug = args[0]

        # check if catalog exists
        try:
            catalog = Catalog.objects.get(slug = catalog_slug)
        except Catalog.DoesNotExist:
            # abort everything
            self.stdout.write("No catalog object found with slug %s. Unable to resequence." % catalog_slug)
            raise

        self.stdout.write('Resequencing cards in "%s"' % catalog_slug)

        catalog_boxes = catalog.boxes.all().order_by('sequence_number')

        catalog_sequence_number = 1

        for box in catalog_boxes:
            for card in box.cards.all().order_by('sequence_number'):
                card.catalog_sequence_number = catalog_sequence_number
                card.save()
                catalog_sequence_number += 1

        self.stdout.write('Done. Last sequence number was %s.' % catalog_sequence_number)
