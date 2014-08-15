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
            result = Card.objects.filter( Q(ocr_text__icontains=query) |
                    Q(name__icontains=query) |
                    Q(arr_tr__icontains=query) |
                    Q(pseudonym_tr__icontains=query) |
                    Q(title_tr__icontains=query))[:100]
        else:
            result = None

    return render_to_response('search.html', locals())


def browse(request, catalog_slug, card_catalog_sequence_number):
    catalog = Catalog.objects.get(slug=catalog_slug)
    card = Card.objects.get(catalog_sequence_number=card_catalog_sequence_number)
    box = card.box


    box_cards = box.cards.all()
    image_url = box.folder_name + "/" + card.filename.replace(".jpg", "_view500.jpg")
    fullres_image_url = box.folder_name + "/" + card.filename

    # find next and previous card
    try:
        previous_card = Card.objects.get(box__catalog__slug=catalog_slug, catalog_sequence_number=card.catalog_sequence_number - 1)
    except Card.DoesNotExist:
        previous_card = None

    try:
        next_card = Card.objects.get(box__catalog__slug=catalog_slug, catalog_sequence_number=card.catalog_sequence_number + 1)
    except Card.DoesNotExist:
        next_card = None

    # find +10 and -10 cards
    try:
        previous10_card = Card.objects.get(box__catalog__slug=catalog_slug, catalog_sequence_number=card.catalog_sequence_number - 10)
    except Card.DoesNotExist:
        previous10_card = None

    try:
        next10_card = Card.objects.get(box__catalog__slug=catalog_slug, catalog_sequence_number=card.catalog_sequence_number + 10)
    except Card.DoesNotExist:
        next10_card = None


    # next and previous box
    try:
        previous_box_card = Card.objects.filter(box__sequence_number = box.sequence_number - 1)[0]
    except:
        previous_box_card = None

    try:
        next_box_card = Card.objects.filter(box__sequence_number = box.sequence_number + 1)[0]
    except:
        next_box_card = None

    return render_to_response('browse.html', locals())



def about(request):

    return render_to_response('about.html', locals())
