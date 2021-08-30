from django import forms
from digipal.views.content_type.search_content_type import get_form_field_from_queryset
from digipal.models import ItemPart, Repository
from digipal.utils import sorted_natural
from mezzanine.conf import settings
from django.db.models import Q

#####################################################
### BONHUM - Rewriting of class FilterManuscripts ###
###                                               ###
### BEGINNING                                     ###
#####################################################

# MODIFICATIONS
# - removed field index

class FilterManuscripts(forms.Form):
    repository = get_form_field_from_queryset([m.human_readable() for m in Repository.objects.filter(currentitem__itempart__isnull=False).order_by('place__name', 'name').distinct()], 'Repository')
    ms_date = get_form_field_from_queryset(sorted_natural(list(ItemPart.objects.filter(historical_items__date__isnull=False, historical_items__date__gt='').values_list('historical_items__date', flat=True).order_by('historical_items__date').distinct())), 'Date')

#####################################################
### END                                           ###
###                                               ###
### BONHUM - Rewriting of class FilterManuscripts ###
#####################################################

#######################################################
### BONHUM - Rewriting of SearchManuscripts methods ###
###                                                 ###
### BEGINNING                                       ###
#######################################################

# MODIFICATIONS
# - get_headings: redefinition of the method to replace "Index" by "Images" and
# to remove "Description"
# - get_form: redefinition of the method in order to use the new FilterManuscripts class
# - added method _build_queryset for the advanced search; it returns ids

from digipal.views.content_type.search_manuscripts import SearchManuscripts


def get_headings(self):
    ret = [
        {'label': 'Images', 'key': 'index', 'is_sortable': False},
        {'label': 'Repository', 'key': 'repository', 'is_sortable': True, 'title': 'Repository and Shelfmark'},
        {'label': 'Shelfmark', 'key': 'shelfmark', 'is_sortable': False},
        {'label': 'Folio(s)', 'key': 'folio', 'is_sortable': False}
    ]
    return getattr(settings, 'SEARCH_ITEM_PART_HEADINGS', ret)

SearchManuscripts.get_headings = get_headings


def get_form(self, request=None):
    initials = None
    if request:
        initials = request.GET
    return FilterManuscripts(initials)

SearchManuscripts.get_form = get_form


def _build_queryset(self, request, term):
    type = self.key
    self.query_phrase = term.strip()
    query_manuscripts = ItemPart.objects.filter(
        Q(locus__contains=term) | \
        Q(current_item__shelfmark__icontains=term) | \
        Q(current_item__repository__name__icontains=term) | \
        Q(historical_items__catalogue_number__icontains=term) | \
        Q(historical_items__description__description__icontains=term) | \
        # name of painters who worked on this item part
        Q(hands__scribe__name__icontains=term) | \
        # name of motives used in this item part
        Q(hands__scribe__idiographs__allograph__name__icontains=term) | \
        # name variants of characters with motives used in this item part
        Q(hands__scribe__idiographs__allograph__bonhum_motivestorycharacter__story_character__bonhum_storycharacternamevariant__name__icontains=term) | \
        # title of texts from this item part
        Q(text__title__icontains=term) | \
        # title of sources linked to texts from this item part
        Q(text__sources__title__icontains=term) | \
        # name of authors of sources linked to texts from this item part
        Q(text__sources__authors__name__icontains=term) | \
        # name of characters linked to texts from this item part
        Q(text__story_characters__name__icontains=term) | \
        # name variants of characters linked to texts from this item part
        Q(text__story_characters__bonhum_storycharacternamevariant__name__icontains=term)
    )

    repository = request.GET.get('repository', '')
    ms_date = request.GET.get('ms_date', '')
    scribe_name = request.GET.get('scribe', '')
    scriptorium = request.GET.get('scriptorium', '')
    scribe_date = request.GET.get('scribe_date', '')
    character = request.GET.get('character', '')
    allograph = request.GET.get('allograph', '')
    chartype = request.GET.get('chartype', '')

    self.is_advanced = repository or ms_date

    if ms_date:
        query_manuscripts = query_manuscripts.filter(historical_items__date=ms_date)
    if repository:
        repository_place = repository.split(',')[0]
        repository_name = repository.split(', ')[1]
        query_manuscripts = query_manuscripts.filter(current_item__repository__name=repository_name, current_item__repository__place__name=repository_place)

    if scribe_name:
        query_manuscripts=query_manuscripts.filter(hands__scribe__name=scribe_name)
    if scriptorium:
        query_manuscripts = query_manuscripts.filter(hands__scribe__scriptorium__name=scriptorium)
    if scribe_date:
        query_manuscripts = query_manuscripts.filter(hands__scribe__date=scribe_date)

    if chartype:
        query_manuscripts = query_manuscripts.filter(hands__scribe__idiographs__allograph__character__ontograph__ontograph_type__name=chartype)
    if character:
        query_manuscripts = query_manuscripts.filter(hands__scribe__idiographs__allograph__character__name=character)
    if allograph:
        query_manuscripts = query_manuscripts.filter(hands__scribe__idiographs__allograph__name=allograph)

    self._queryset = list(query_manuscripts.distinct().order_by('display_label').values_list('id', flat=True))

    return self._queryset

SearchManuscripts._build_queryset = _build_queryset

#######################################################
### END                                             ###
###                                                 ###
### BONHUM - Rewriting of SearchManuscripts methods ###
#######################################################
