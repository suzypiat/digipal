from django import forms
from digipal.views.content_type.search_content_type import SearchContentType, \
get_form_field_from_queryset
from digipal_text.models import TextContentXML
from digipal_project.models import Bonhum_StoryPlace, Bonhum_StoryCharacter
from django.db.models import Q
import re

class FilterPlaces(forms.Form):
    place = get_form_field_from_queryset(Bonhum_StoryPlace.objects.values_list('name', flat=True).order_by('name').distinct(), 'Place')
    type = get_form_field_from_queryset(Bonhum_StoryPlace.objects.values_list('type__name', flat=True).order_by('type__name').distinct(), 'Type', aid='type')
    nature = get_form_field_from_queryset(Bonhum_StoryPlace.objects.values_list('nature__name', flat=True).order_by('nature__name').distinct(), 'Nature', aid='nature')

class SearchPlaces(SearchContentType):

    def get_fields_info(self):
        ''' See SearchContentType.get_fields_info() for a description of the field structure '''
        ret = super(SearchPlaces, self).get_fields_info()
        return ret

    def get_sort_fields(self):
        ''' returns a list of django field names necessary to sort the results '''
        return ['name']

    def set_record_view_context(self, context, request):
        super(SearchPlaces, self).set_record_view_context(context, request)
        place = Bonhum_StoryPlace.objects.get(id=context['id'])
        context['place'] = place

        context['characters'] = {
            'by_geographical_origin': sorted(place.bonhum_storycharacter_set.all(),
                                      key=lambda c: c.name),
            'by_text': []
        }

        from bs4 import BeautifulSoup
        text_content_xmls = TextContentXML.objects.all()
        texts = []
        for tcx in text_content_xmls:
            soup = BeautifulSoup(tcx.content, 'lxml')
            # We get the <placeName> annotations related to the place
            # (i.e. when the ref attribute starts with the place id)
            spans = soup.find_all('span', attrs={ 'data-dpt': 'placeName',
                                                   'data-dpt-ref': re.compile(ur'^#'
                                                   + str(place.id) + ur'\b.*?')})

            if len(spans) > 0:
                annotations = []
                for span in spans:
                    content = span.get_text()
                    in_relation_with = []
                    ref = span.attrs.get('data-dpt-ref').split(' ')
                    ref.pop(0)
                    # If ref contains other ids than the one of the place, we extract
                    # all the ids in the ref attribute and get the matching characters in database
                    if len(ref) > 0:
                        ref = [ int(id[1:]) for id in ref ]
                        in_relation_with = [ Bonhum_StoryCharacter.objects.get(id=id) for id in ref ]
                        context['characters']['by_text'] += in_relation_with
                    annotations.append({
                        'content': content, 'in_relation_with': in_relation_with
                    })
                texts.append({
                    'text_content_xml': tcx,
                    'annotations': annotations
                })

        context['texts'] = texts
        context['characters']['by_text'] = sorted(set(context['characters']['by_text']),
                                           key=lambda c: c.name)
        context['nb_characters'] = len(set(context['characters']['by_geographical_origin']
                                   + context['characters']['by_text']))

    def get_model(self):
        return Bonhum_StoryPlace

    def get_form(self, request=None):
        initials = None
        if request:
            initials = request.GET
        return FilterPlaces(initials)

    @property
    def key(self):
        return 'places'

    @property
    def label(self):
        return 'Places'

    @property
    def label_singular(self):
        return 'Place'

    def _build_queryset_django(self, request, term):
        type = self.key
        query_places = Bonhum_StoryPlace.objects.filter(
                    Q(name__icontains=term) | \
                    Q(type__name__icontains=term) | \
                    Q(nature__name__icontains=term))

        name = request.GET.get('name', '')
        type = request.GET.get('type', '')
        nature = request.GET.get('nature', '')

        if name:
            query_places = query_places.filter(name=name)
        if type:
            query_places = query_places.filter(type__name=type)
        if nature:
            query_places = query_places.filter(nature__name=nature)

        self._queryset = query_places.distinct().order_by('name')

        return self._queryset