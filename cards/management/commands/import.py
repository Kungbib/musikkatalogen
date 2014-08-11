# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from cards.models import *
import os
from os import listdir
from os.path import isfile, join


class Command(BaseCommand):
    help = 'Import folders of catalog cards to a specific catalog.'
    args = '<path> <catalog_slug>'

    def add_arguments(self, parser):
        parser.add_argument('path')
        parser.add_argument('catalog_slug')

    def handle(self, *args, **options):

        path = args[0]
        catalog_slug = args[1]

        self.stdout.write('Importing "%s" to catalog %s' % (path, catalog_slug))

        #check if path exists
        if not os.path.isdir(path):
            raise CommandError("Path %s does not exist" % path)

        # check if catalog exists
        try:
            catalog = Catalog.objects.get(slug = catalog_slug)
        except Catalog.DoesNotExist:
            # abort everything
            self.stdout.write("No catalog object found with slug %s. Unable to import box." % catalog_slug)
            raise

        #get folder name
        folder = os.path.split(path)[-1]

        self.stdout.write('Importing "%s"' % folder)

        #check if folder name exists
        try:
            box = Box.objects.get(folder_name=folder, catalog=catalog)

            self.stdout.write('Loaded existing box "%s"' % box.id)
        except Box.DoesNotExist:

            # make it - assumes folder name
            # <sequence number>_<project name>_<label>
            # 0027_musik-alfa_FLODI-FORO

            print folder
            sequence_number = int(folder.split("_")[0])
            label = folder.split("_")[2]

            box = Box(folder_name=folder,
                    sequence_number=sequence_number,
                    label=label,
                    slug=label,
                    catalog=catalog)
            box.save()

            self.stdout.write('Created box "%s"' % box.id)


        #import folder content and create cards

        for f in listdir(path):
            if isfile(join(path,f)):
                if f.endswith(".jpg") and not "_view" in f and not "_clean.jpg" in f:
                    try:
                        card = Card.objects.get(box=box, filename=f)
                    except Card.DoesNotExist:
                        #make it
                        card = Card(filename=f,box=box)

                    # parse sequence number in box
                    sequence_number = int(f.split("_")[-1].replace(".jpg",""))
                    card.sequence_number=sequence_number

                    # get corresponding ocr file
                    ocr_filename = f.replace(".jpg","_cleanocr.txt")

                    if os.path.isfile(path + "/" + ocr_filename):
                        with open(path + "/" + ocr_filename, 'r') as ocrfile:
                            ocr_text = ocrfile.read()

                        card.ocr_text=ocr_text
                        card.name=ocr_text.split("\n")[0].strip()
                    else:
                        card.name="%s [handskrivet]" % box.label

                    card.save()
