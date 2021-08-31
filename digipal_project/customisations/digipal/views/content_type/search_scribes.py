from django import forms
from digipal.views.content_type.search_content_type import get_form_field_from_queryset
from digipal.utils import sorted_natural
from digipal.models import Scribe, Allograph
from django.db.models import Q

#################################################
### BONHUM - Rewriting of class FilterScribes ###
###                                           ###
### BEGINNING                                 ###
#################################################

# MODIFICATIONS
# - added a filter on field scribe to display only painters, not scribes
# - renamed fields scribe, scriptorium, chartype and character
# - added field allograph
# - removed fields component and feature

class FilterScribes(forms.Form):
    scribe = get_form_field_from_queryset(Scribe.objects.exclude(type__name__icontains='scribe').values_list('name', flat=True).order_by('name').distinct(), 'Painter')
    scriptorium = get_form_field_from_queryset(Scribe.objects.values_list('scriptorium__name', flat=True).order_by('scriptorium__name').distinct(), 'Workshop')
    scribe_date = get_form_field_from_queryset(sorted_natural(list(Scribe.objects.filter(date__isnull=False).values_list('date', flat=True).order_by('date').distinct())), 'Date')
    chartype = get_form_field_from_queryset(Scribe.objects.values_list('idiographs__allograph__character__ontograph__ontograph_type__name', flat= True).order_by('idiographs__allograph__character__ontograph__ontograph_type__name').distinct(), 'Macro Category Type', aid='chartype')
    character = get_form_field_from_queryset(Scribe.objects.values_list('idiographs__allograph__character__name', flat=True).order_by('idiographs__allograph__character__ontograph__sort_order').distinct(), 'Category', aid='character')
    allograph = get_form_field_from_queryset(Scribe.objects.values_list('idiographs__allograph__name', flat=True).order_by('idiographs__allograph__name').distinct(), 'Motive', aid='allograph')

#################################################
### END                                       ###
###                                           ###
### BONHUM - Rewriting of class FilterScribes ###
#################################################

###################################################
### BONHUM - Rewriting of SearchScribes methods ###
###                                             ###
### BEGINNING                                   ###
###################################################

# MODIFICATIONS
# - get_form: redefinition of the method in order to use the new FilterScribes class
# - label: changed "Scribes" to "Painters"
# - label_singular: changed "Scribe" to "Painter"
# - added method _build_queryset for the advanced search, with a filter to display
# only painters, not scribes; it returns ids

from digipal.views.content_type.search_scribes import SearchScribes


def get_form(self, request=None):
    initials = None
    if request:
        initials = request.GET
    return FilterScribes(initials)

SearchScribes.get_form = get_form


@property
def label(self):
    return 'Painters'

SearchScribes.label = label


@property
def label_singular(self):
    return 'Painter'

SearchScribes.label_singular = label_singular


def _build_queryset(self, request, term):
    type = self.key
    query_scribes = Scribe.objects.exclude(type__name__icontains='scribe')
    query_scribes = query_scribes.filter(
        Q(name__icontains=term) | \
        Q(scriptorium__name__icontains=term) | \
        Q(date__icontains=term) | \
        Q(hands__item_part__work_current_item__current_item__shelfmark__icontains=term) | \
        Q(hands__item_part__work_current_item__current_item__repository__name__icontains=term) | \
        Q(hands__item_part__historical_items__catalogue_number__icontains=term) | \
        # name of motives used by the painter
        Q(idiographs__allograph__name__icontains=term) | \
        # name variants of characters with motives used by the painter
        Q(idiographs__allograph__bonhum_motivestorycharacter__story_character__bonhum_storycharacternamevariant__name__icontains=term)
    )

    scribe_name = request.GET.get('scribe', '')
    scriptorium = request.GET.get('scriptorium', '')
    scribe_date = request.GET.get('scribe_date', '')
    ms_date = request.GET.get('ms_date', '')
    repository = request.GET.get('repository', '')
    character = request.GET.get('character', '')
    allograph = request.GET.get('allograph', '')
    chartype = request.GET.get('chartype', '')

    self.is_advanced = scribe_name or scriptorium or scribe_date or character

    if scribe_name:
        query_scribes = query_scribes.filter(name=scribe_name)
    if scriptorium:
        query_scribes = query_scribes.filter(scriptorium__name=scriptorium)
    if scribe_date:
        query_scribes = query_scribes.filter(date=scribe_date)

    if ms_date:
        query_scribes = query_scribes.filter(hands__item_part__historical_items__date=ms_date)
    if repository:
        repository_place = repository.split(',')[0]
        repository_name = repository.split(', ')[1]
        query_scribes = query_scribes.filter(hands__item_part__work_current_item__current_item__repository__name=repository_name, hands__item_part__work_current_item__current_item__repository__place__name=repository_place)

    if chartype:
        query_scribes = query_scribes.filter(idiographs__allograph__character__ontograph__ontograph_type__name=chartype)
    if character:
        query_scribes = query_scribes.filter(idiographs__allograph__character__name=character)
    if allograph:
        query_scribes = query_scribes.filter(idiographs__allograph__name=allograph)

    self._queryset = list(query_scribes.distinct().order_by('name').values_list('id', flat=True))

    return self._queryset

SearchScribes._build_queryset = _build_queryset

###################################################
### END                                         ###
###                                             ###
### BONHUM - Rewriting of SearchScribes methods ###
###################################################
