from django import forms
from digipal.views.content_type.search_content_type import get_form_field_from_queryset
from digipal.models import Graph, Allograph, Image, MediaPermission
from digipal.templatetags.hand_filters import chrono
from django.forms.widgets import Select
from django.db.models import Q
import re

################################################
### BONHUM - Rewriting of class FilterGraphs ###
###                                          ###
### BEGINNING                                ###
################################################

# MODIFICATIONS
# - removed field script
# - renamed fields chartype, character and allograph

class FilterGraphs(forms.Form):
    chartype = get_form_field_from_queryset(Graph.objects.values_list('idiograph__allograph__character__ontograph__ontograph_type__name', flat=True).order_by(
        'idiograph__allograph__character__ontograph__ontograph_type__name').distinct(), 'Macro Category Type', aid='chartype')
    character = get_form_field_from_queryset(Graph.objects.values_list('idiograph__allograph__character__name', flat=True).order_by(
        'idiograph__allograph__character__ontograph__sort_order').distinct(), 'Category', aid='character')
    allograph = forms.ChoiceField(
        choices=[('', 'Motive')] + [(m.name, m.human_readable())
                                       for m in Allograph.objects.filter(idiograph__graph__isnull=False).exclude(hidden=True).distinct()],
        widget=Select(attrs={'id': 'allograph', 'class': 'chzn-select',
                             'data-placeholder': 'Choose a Motive'}),
        label='', initial='Motive', required=False
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
# - _build_queryset: added fields to look for the search term

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


def _build_queryset(self, request, term):
    """ View for Hand record drill-down """
    context = {}
    self.graphs_count = 0

    undefined = u''

    scribe = request.GET.get('scribe', undefined)
    # alternative names are for backward compatibility with old-style graph
    # search page
    script = request.GET.get('script', undefined)
    chartype = request.GET.get('chartype', undefined)
    character = request.GET.get('character', undefined)
    allograph = request.GET.get('allograph', undefined)
    component = request.GET.get('component', undefined)
    feature = request.GET.get('feature', undefined)
    repository = request.GET.get('repository', undefined)
    index = request.GET.get('index', undefined)

    excluded_images = None
    from digipal.utils import is_staff
    if not is_staff(request):
        excluded_images = Image.filter_permissions(
            Image.objects.all(), [MediaPermission.PERM_PRIVATE])

    none = u'-1'
    one_or_more = u'-2'

    from datetime import datetime

    t0 = datetime.now()
    t4 = datetime.now()

    wheres = []

    if self.search_hands:
        graphs = Graph.objects.filter(
            hand__id__in=self.search_hands.queryset)
    else:

        # .order_by('item_part__current_item__repository__name', 'item_part__current_item__shelfmark', 'descriptions__description','id')
        # Although we are listing hands on the front-end, we search for graphs and not for hand.
        # Two reasons:
        #    searching for character and allograh at the same time through a Hand model would generate two separate joins to graph
        #        this would bring potentially invalid results and it is also much slower
        #    it is faster than excluding all the hands without a graph (yet another expensive join)
        #
        if term:
            term = term.replace('"', '')
            graphs = Graph.objects.filter(
                Q(hand__descriptions__description__icontains=term) |
                Q(hand__scribe__name__icontains=term) |
                Q(hand__assigned_place__name__icontains=term) |
                Q(hand__assigned_date__date__icontains=term) |
                Q(hand__item_part__current_item__shelfmark__icontains=term) |
                Q(hand__item_part__current_item__repository__name__icontains=term) |
                Q(hand__item_part__current_item__repository__place__name__icontains=term) |
                Q(hand__item_part__historical_items__catalogue_number__icontains=term) | \
                # JIRA 423
                Q(hand__item_part__historical_items__name__icontains=term) | \
                Q(hand__item_part__group__historical_items__name__icontains=term) | \
                Q(hand__item_part__display_label__icontains=term) | \
                Q(hand__item_part__group__display_label__icontains=term) | \

                # BONHUM - Added fields
                # name of motives
                Q(idiograph__allograph__name__icontains=term) | \
                # name variants of characters with motives
                Q(idiograph__allograph__bonhum_motivestorycharacter__story_character__bonhum_storycharacternamevariant__name__icontains=term) | \
                # name of components
                Q(graph_components__component__name__icontains=term) | \
                # name of features
                Q(graph_components__features__name__icontains=term)
            )
        else:
            graphs = Graph.objects.all()

        t1 = datetime.now()

        if index:
            graphs = graphs.filter(
                hand__item_part__historical_items__catalogue_number__iexact=index)
        if repository:
            matches = re.match(ur'^([^,]+?),([^,]+)$', repository)
            if matches:
                graphs = graphs.filter(Q(hand__item_part__current_item__repository__place__name__iexact=matches.group(
                    1).strip()) & Q(hand__item_part__current_item__repository__name__iexact=matches.group(2).strip()))
        if scribe:
            graphs = graphs.filter(hand__scribe__name__icontains=scribe)
        if script:
            graphs = graphs.filter(hand__script__name=script)

    if chartype:
        graphs = graphs.filter(
            idiograph__allograph__character__ontograph__ontograph_type__name=chartype)
    if character:
        graphs = graphs.filter(
            idiograph__allograph__character__name=character)
    if allograph:
        graphs = graphs.filter(idiograph__allograph__name=allograph)

    # we discard freak graph records (i.e. without annotation) to prevent
    # errors further down the line.
    graphs = graphs.filter(annotation__isnull=False)

    # if the user is not logged in we exclude graphs where the allograph is
    # hidden
    from digipal.models import has_edit_permission
    if not has_edit_permission(request, self.get_model()):
        graphs = graphs.exclude(idiograph__allograph__hidden=True)

    # exclude private images
    if excluded_images and excluded_images.count():
        graphs = graphs.exclude(annotation__image__in=excluded_images)

    # condition on component
    if component:
        component_where = Q(graph_components__component__name=component)
        if feature in [undefined, none]:
            # If no feature is specified we find all the graph which are supposed to have a component
            # according to their idiograph
            component_where = component_where | Q(
                idiograph__allograph__allograph_components__component__name=component)
        wheres.append(component_where)

    # condition on feature
    if feature not in [undefined, none, one_or_more]:
        wheres.append(Q(graph_components__features__name=feature))
    if feature in [one_or_more]:
        wheres.append(Q(graph_components__features__id__isnull=False))

    # ANDs all the Q() where clauses together
    if wheres:
        where_and = wheres.pop(0)
        for where in wheres:
            where_and = where_and & where

        graphs = graphs.filter(where_and)

    # Treat the feature=none case
    if feature == none:
        excluded_q = Q(graph_components__features__id__isnull=False)
        if component:
            excluded_q = excluded_q & Q(
                graph_components__component__name=component)
        excluded_graphs = Graph.objects.filter(excluded_q)
        graphs = graphs.exclude(
            id__in=excluded_graphs.values_list('id', flat=True))

    from digipal.utils import set_left_joins_in_queryset, get_str_from_queryset
    set_left_joins_in_queryset(graphs)
    # print get_str_from_queryset(graphs)

    t2 = datetime.now()

    # Get the graphs then id of all the related Hands
    # We use values_list because it is much faster, we don't need to fetch all the Hands at this stage
    # That will be done after pagination in the template
    # Distinct is needed here.
    #graphs = graphs.distinct().order_by('hand__scribe__name', 'hand__id', 'idiograph__allograph__character__ontograph__sort_order')
    chrono('graph filter:')
    graphs = graphs.distinct().order_by('hand__scribe__name', 'hand__id')
    chrono(':graph filter')

    # print graphs.query
    chrono('graph values_list:')
    graph_ids = graphs.values_list('id', 'hand_id')
    chrono(':graph values_list')

#        chrono('len:')
#        l = len(graph_ids)
#        print graph_ids.query
#        chrono(':len')

    # Build a structure that groups all the graph ids by hand id
    # context['hand_ids'] = [[1, 101, 102], [2, 103, 104]]
    # In the above we have two hands: 1 and 2. For hand 1 we have Graph 101
    # and 102.
    chrono('hand_ids:')
    context['hand_ids'] = [[0]]
    last = 0
    for g in graph_ids:
        if g[1] != context['hand_ids'][-1][0]:
            context['hand_ids'].append([g[1]])
        context['hand_ids'][-1].append(g[0])
    del(context['hand_ids'][0])
    chrono(':hand_ids')

    t3 = datetime.now()

    self.graphs_count = len(graph_ids)

    t4 = datetime.now()

    # print 'search %s; hands query: %s + graph count: %s' % (t4 - t0, t3 -
    # t2, t4 - t3)

    t5 = datetime.now()
    self._queryset = context['hand_ids']

    return self._queryset

SearchGraphs._build_queryset = _build_queryset

##################################################
### END                                        ###
###                                            ###
### BONHUM - Rewriting of SearchGraphs methods ###
##################################################
