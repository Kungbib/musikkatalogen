# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from cards.models import *
from django.db.models import Q

def index(request):

    # Read alphabet index cards
    index_cards = Card.objects.filter(letter__isnull=False).exclude(letter='').order_by("letter")

    # Read boxes
    boxes = Box.objects.all().order_by("sequence_number")
    return render_to_response('index.html', locals())


def search(request):
    # get query
    if request.GET.get('q'):
        query = request.GET.get('q', None).strip()
        if query:
            #result = Card.objects.filter(ocr_text__icontains=query)[:100]
            result = Card.objects.filter( Q(ocr_text__icontains=query) | Q(name__icontains=query) )[:100]
        else:
            result = None

    return render_to_response('search.html', locals())


def browse(request, catalog_slug, box_sequence_number, card_catalog_sequence_number):
    catalog = Catalog.objects.get(slug=catalog_slug)
    box = Box.objects.get(catalog=catalog, sequence_number=box_sequence_number)

    card = Card.objects.get(box=box, catalog_sequence_number=card_catalog_sequence_number)

    box_cards = box.cards.all()
    image_url = box.folder_name + "/" + card.filename.replace(".jpg", "_view500.jpg")
    fullres_image_url = box.folder_name + "/" + card.filename

    # find next and previous card
    if card.catalog_sequence_number > 0:
        previous_card = Card.objects.get(box__catalog__slug=catalog_slug, catalog_sequence_number=card.catalog_sequence_number - 1)
    else:
        previous_card = None

    try:
        next_card = Card.objects.get(box__catalog__slug=catalog_slug, catalog_sequence_number=card.catalog_sequence_number + 1)
    except Card.DoesNotExist:
        next_card = None

    # find +10 and -10 cards
    if card.catalog_sequence_number > 10:
        previous10_card = Card.objects.get(box__catalog__slug=catalog_slug, catalog_sequence_number=card.catalog_sequence_number - 10)
    else:
        previous10_card = None

    try:
        next10_card = Card.objects.get(box__catalog__slug=catalog_slug, catalog_sequence_number=card.catalog_sequence_number + 10)
    except Card.DoesNotExist:
        next10_card = None

    return render_to_response('browse.html', locals())

