from django import forms
from digipal.views.content_type.search_content_type import get_form_field_from_queryset
from digipal.utils import sorted_natural
from digipal.models import Scribe

#################################################
### BONHUM - Rewriting of class FilterScribes ###
###                                           ###
### BEGINNING                                 ###
#################################################

# MODIFICATIONS
# - added a filter in order to display only contributors whose type is "painter"
# - renamed field scriptorium
# - renamed field chartype
# - renamed field character

class FilterScribes(forms.Form):
    scribe = get_form_field_from_queryset(Scribe.objects.filter(type__name='Peintre').values_list('name', flat=True).order_by('name').distinct(), 'Painter')
    scriptorium = get_form_field_from_queryset(Scribe.objects.values_list('scriptorium__name', flat=True).order_by('scriptorium__name').distinct(), 'Workshop')
    scribe_date = get_form_field_from_queryset(sorted_natural(list(Scribe.objects.filter(date__isnull=False).values_list('date', flat=True).order_by('date').distinct())), 'Date')
    chartype = get_form_field_from_queryset(Scribe.objects.values_list('idiographs__allograph__character__ontograph__ontograph_type__name', flat= True).order_by('idiographs__allograph__character__ontograph__ontograph_type__name').distinct(), 'Macro Category Type', aid='chartype')
    character = get_form_field_from_queryset(Scribe.objects.values_list('idiographs__allograph__character__name', flat=True).order_by('idiographs__allograph__character__ontograph__sort_order').distinct(), 'Category', aid='character')
    component = get_form_field_from_queryset(Scribe.objects.values_list('idiographs__idiographcomponent__component__name', flat=True).order_by('idiographs__idiographcomponent__component__name').distinct(), 'Component')
    feature = get_form_field_from_queryset(Scribe.objects.values_list('idiographs__idiographcomponent__features__name', flat=True).order_by('idiographs__idiographcomponent__features__name').distinct(), 'Feature')

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
# - _build_queryset_django: added a filter in order to display only contributors whose type is "painter"

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


def _build_queryset_django(self, request, term):
    type = self.key
    query_scribes = Scribe.objects.filter(type__name='Peintre').filter(
                Q(name__icontains=term) | \
                Q(scriptorium__name__icontains=term) | \
                Q(date__icontains=term) | \
                Q(hand__item_part__current_item__shelfmark__icontains=term) | \
                Q(hand__item_part__current_item__repository__name__icontains=term) | \
                Q(hand__item_part__historical_item__catalogue_number__icontains=term))

    name = request.GET.get('name', '')
    scriptorium = request.GET.get('scriptorium', '')
    date = request.GET.get('date', '')
    character = request.GET.get('character', '')
    component = request.GET.get('component', '')
    feature = request.GET.get('feature', '')

    self.is_advanced = name or scriptorium or date or character or component or feature

    if name:
        query_scribes = query_scribes.filter(name=name)
    if scriptorium:
        query_scribes = query_scribes.filter(scriptorium__name=scriptorium)
    if date:
        query_scribes = query_scribes.filter(date=date)
    if character:
        query_scribes = query_scribes.filter(idiographs__allograph__character__name=character)
    if component:
        query_scribes = query_scribes.filter(idiographs__allograph__allographcomponent__component__name=component)
    if feature:
        query_scribes = query_scribes.filter(idiographs__allograph__allographcomponent__component__features__name=feature)

    self._queryset = query_scribes.distinct().order_by('name')

    return self._queryset

SearchScribes._build_queryset_django = _build_queryset_django

###################################################
### END                                         ###
###                                             ###
### BONHUM - Rewriting of SearchScribes methods ###
###################################################
