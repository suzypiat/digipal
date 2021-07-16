from django import forms
from digipal.views.content_type.search_content_type import get_form_field_from_queryset
from digipal.models import Graph, Allograph
from django.forms.widgets import Select

################################################
### BONHUM - Rewriting of class FilterGraphs ###
###                                          ###
### BEGINNING                                ###
################################################

# MODIFICATIONS
# - renamed field chartype
# - renamed field character
# - renamed field allograph

class FilterGraphs(forms.Form):
    script = get_form_field_from_queryset(Graph.objects.values_list(
        'hand__script__name', flat=True).order_by('hand__script__name').distinct(), 'Script', aid='script')
    chartype = get_form_field_from_queryset(Graph.objects.values_list('idiograph__allograph__character__ontograph__ontograph_type__name', flat=True).order_by(
        'idiograph__allograph__character__ontograph__ontograph_type__name').distinct(), 'Macro Category Type', aid='chartype')
    character = get_form_field_from_queryset(Graph.objects.values_list('idiograph__allograph__character__name', flat=True).order_by(
        'idiograph__allograph__character__ontograph__sort_order').distinct(), 'Category', aid='character')
    allograph = forms.ChoiceField(
        choices=[("", "Motive")] + [(m.name, m.human_readable())
                                       for m in Allograph.objects.filter(idiograph__graph__isnull=False).exclude(hidden=True).distinct()],
        widget=Select(attrs={'id': 'allograph', 'class': 'chzn-select',
                             'data-placeholder': "Choose a Motive"}),
        label='',
        initial='Allograph',
        required=False
    )
    component = get_form_field_from_queryset(Graph.objects.exclude(idiograph__allograph__hidden=True).values_list(
        'graph_components__component__name', flat=True).order_by('graph_components__component__name').distinct(), 'Component', aid='component')
    feature = get_form_field_from_queryset(Graph.objects.exclude(idiograph__allograph__hidden=True).values_list('graph_components__features__name', flat=True).order_by(
        'graph_components__features__name').distinct(), 'Feature', aid='feature', other_choices=[(-1, 'No Features'), (-2, 'One of more features')])

################################################
### END                                      ###
###                                          ###
### BONHUM - Rewriting of class FilterGraphs ###
################################################

##################################################
### BONHUM - Rewriting of SearchGraphs methods ###
###                                            ###
### BEGINNING                                  ###
##################################################

# MODIFICATIONS
# - get_form: redefinition of the method in order to use the new FilterGraphs class
# - label: changed "Graphs" to "Iconography"
# - label_singular: changed "Graph" to "Iconography"
# - added method get_model to return "Graph" and not "Iconograph", since the label has been overwritten

from digipal.views.content_type.search_graphs import SearchGraphs


def get_form(self, request=None):
    initials = None
    if request:
        initials = request.GET
    return FilterGraphs(initials)

SearchGraphs.get_form = get_form


@property
def label(self):
    return 'Iconography'

SearchGraphs.label = label


@property
def label_singular(self):
    return 'Iconography'

SearchGraphs.label_singular = label_singular


def get_model(self):
    return Graph

SearchGraphs.get_model = get_model

##################################################
### END                                        ###
###                                            ###
### BONHUM - Rewriting of SearchGraphs methods ###
##################################################
