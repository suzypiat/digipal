from django import forms
from digipal.views.content_type.search_content_type import SearchContentType, \
get_form_field_from_queryset
from digipal_text.models import TextContentXML
from digipal_project.models import Bonhum_StoryCharacter, Bonhum_StoryPlace
from django.db.models import Q
from mezzanine.conf import settings
from collections import OrderedDict
import re

class FilterCharacters(forms.Form):
    character = get_form_field_from_queryset(Bonhum_StoryCharacter.objects.values_list('name', flat=True).order_by('name').distinct(), 'Character')
    age = get_form_field_from_queryset(Bonhum_StoryCharacter.objects.values_list('age__name', flat=True).order_by('age__name').distinct(), 'Age', aid='age')
    gender = get_form_field_from_queryset(Bonhum_StoryCharacter.objects.values_list('gender__name', flat=True).order_by('gender__name').distinct(), 'Gender', aid='gender')
    religion = get_form_field_from_queryset(Bonhum_StoryCharacter.objects.values_list('religion__name', flat=True).order_by('religion__name').distinct(), 'Religion', aid='religion')
    type = get_form_field_from_queryset(Bonhum_StoryCharacter.objects.values_list('type__name', flat=True).order_by('type__name').distinct(), 'Type', aid='type')
    place = get_form_field_from_queryset(Bonhum_StoryCharacter.objects.values_list('geographical_origin__name', flat=True).order_by('geographical_origin__name').distinct(), 'Place', aid='place')

class SearchCharacters(SearchContentType):

    def get_fields_info(self):
        ''' See SearchContentType.get_fields_info() for a description of the field structure '''
        ret = super(SearchCharacters, self).get_fields_info()
        return ret

    def get_sort_fields(self):
        ''' returns a list of django field names necessary to sort the results '''
        return ['name']

    def set_record_view_context(self, context, request):
        super(SearchCharacters, self).set_record_view_context(context, request)
        character = Bonhum_StoryCharacter.objects.get(id=context['id'])
        context['character'] = character

        context['graphs'] = character.get_graphs()

        text_content_xmls = TextContentXML.objects.filter(text_content__text__id__in=character.texts.values_list('id'))
        context['text_content_xmls'] = text_content_xmls

        # We get the buttons used to annotate the texts
        TE_buttons = settings.TEXT_EDITOR_OPTIONS_CUSTOM['buttons']
        # We get the categories of three buttons: person, time and place
        categories = TE_buttons['btnPerson']['categories'] + TE_buttons['btnTime']['categories'] + TE_buttons['btnPlace']['categories']

        # For each category, we get all its items (ana code and label) and add them to our characteristics
        characteristics = []
        for category in categories:
            codes = OrderedDict()
            for item in category['items']:
                if item['id'] != 'btnPersonName':
                    codes.update({
                        item['attributes']['ana']: { 'label': item['label'], 'annotations': {}, 'nb': 0 }
                    })
                else:
                    codes.update({
                        'person_name': { 'label': item['label'], 'annotations': {}, 'nb': 0 }
                    })
            label = category['label']
            if len(label) == 0:
                label = 'Time' if category['items'][0]['tag'] == 'date' else 'Place'
            characteristics.append({
                'label': label,
                'codes': codes,
                'nb': 0
            })

        # Types of social relationships
        social_types = [
            '#PROS-EV-REL-TY-SOC',
            '#PROS-EV-REL-TY-SOC-TY-PRO',
            '#PROS-EV-REL-TY-SOC-TY-INST',
            '#PROS-EV-REL-TY-SOC-TY-AMOR',
            '#PROS-EV-REL-TY-SOC-TY-AMIC',
            '#PROS-EV-REL-TY-SOC-TY-HOST'
        ]

        # Levels of social relationships
        social_levels = {
            '#PROS-EV-REL-TY-SOC-N-AVECI': 'With an inferior',
            '#PROS-EV-REL-TY-SOC-N-AVECS': 'With a superior',
            '#PROS-EV-REL-TY-SOC-N-AVECP': 'With an equal'
        }

        # Inverses of social relationships levels, to determine the code to use when
        # the character is the object of the annotation
        # e.g. "A is the superior of B" -> B is the inferior of A
        social_levels_inverses = {
            '#PROS-EV-REL-TY-SOC-N-AVECI': '#PROS-EV-REL-TY-SOC-N-AVECS',
            '#PROS-EV-REL-TY-SOC-N-AVECS': '#PROS-EV-REL-TY-SOC-N-AVECI',
            '#PROS-EV-REL-TY-SOC-N-AVECP': '#PROS-EV-REL-TY-SOC-N-AVECP'
        }

        # Inverses of familial relationships, to determine the code to use when
        # the character is the object of the annotation
        # e.g. "A is the child of B" -> B is the parent of A
        # e.g. "A is the nephew of B" -> if B has 1 as gender, B is the uncle of A;
        # if B has 2 as gender, B is the aunt of A (if no gender is given, the default is 1)
        familial_inverses = {
            '#PROS-EV-REL-TY-FAM-PAR': '#PROS-EV-REL-TY-FAM-ENF',
            '#PROS-EV-REL-TY-FAM-ENF': '#PROS-EV-REL-TY-FAM-PAR',
            '#PROS-EV-REL-TY-FAM-GRPAR': '#PROS-EV-REL-TY-FAM-PTSENF',
            '#PROS-EV-REL-TY-FAM-PTSENF': '#PROS-EV-REL-TY-FAM-GRPAR',
            '#PROS-EV-REL-TY-FAM-NIEC': { 1: '#PROS-EV-REL-TY-FAM-ONC', 2: '#PROS-EV-REL-TY-FAM-TAN' },
            '#PROS-EV-REL-TY-FAM-NEV': { 1: '#PROS-EV-REL-TY-FAM-ONC', 2: '#PROS-EV-REL-TY-FAM-TAN' },
            '#PROS-EV-REL-TY-FAM-TAN': { 1: '#PROS-EV-REL-TY-FAM-NEV', 2: '#PROS-EV-REL-TY-FAM-NIEC' },
            '#PROS-EV-REL-TY-FAM-ONC': { 1: '#PROS-EV-REL-TY-FAM-NEV', 2: '#PROS-EV-REL-TY-FAM-NIEC' }
        }

        from bs4 import BeautifulSoup
        # For each text_content_xml linked to the character
        for tcx in text_content_xmls:
            soup = BeautifulSoup(tcx.content, 'lxml')
            # We get the <rs> annotations in which the character is subject
            # (i.e. when the ref attribute starts with the character id)
            rs_subject_spans = soup.find_all('span', attrs={ 'data-dpt': 'rs',
                                                   'data-dpt-ref': re.compile(ur'^#'
                                                   + str(character.id) + ur'\b.*?')})
            # We get the <rs> annotations in which the character is object
            # (i.e. when the ref attribute includes the character id, but NOT in first position)
            rs_object_spans = soup.find_all('span', attrs={ 'data-dpt': 'rs',
                                                   'data-dpt-ref': re.compile(ur'(?!#'
                                                   + str(character.id) + ur'\b).*?#'
                                                   + str(character.id) + ur'\b.*?')})
            # We get the <persName> annotations in which the ref attribute is the character id
            persname_spans = soup.find_all('span', attrs={ 'data-dpt': 'persName',
                                                   'data-dpt-ref': '#' + str(character.id)})
            # We get the <date> annotations related to the character
            # (i.e. when the ref attribute includes the character id)
            date_spans = soup.find_all('span', attrs={ 'data-dpt': 'date',
                                                   'data-dpt-ref': re.compile(ur'.*?#'
                                                   + str(character.id) + ur'\b.*?')})
            # We get the <placeName> annotations related to the character
            # (i.e. when the ref attribute includes the character id,
            # but NOT in first position, since the first id is the one of the place)
            place_spans = soup.find_all('span', attrs={ 'data-dpt': 'placeName',
                                                   'data-dpt-ref': re.compile(ur'(?!#'
                                                   + str(character.id) + ur'\b).*?#'
                                                   + str(character.id) + ur'\b.*?')})

            # For each <persName>, <placeName> and <date> annotation
            spans = persname_spans + place_spans + date_spans
            for span in spans:
                tag = span.attrs.get('data-dpt')
                code = span.attrs.get('data-dpt-ana') if tag != 'persName' else 'person_name'
                content = span.get_text()
                data = { 'content': content }
                # If the annotation is <placeName>, we extract the first id
                # in the ref attribute and get the matching place in database
                if tag == 'placeName':
                    ref = span.attrs.get('data-dpt-ref').split(' ')
                    place_id = int(ref.pop(0)[1:])
                    place = Bonhum_StoryPlace.objects.get(id=place_id)
                    data['place'] = place
                # We add the related text segment to our characteristics regarding
                # the code in the ana attribute, with the related place for <placeName>
                for category in characteristics:
                    if code in category['codes'].keys():
                        category['codes'][code]['annotations'].setdefault(tcx, []).append(data)
                        category['codes'][code]['nb'] += 1
                        category['nb'] += 1

            # For each <rs> annotation (with the character as subject or object)
            spans = rs_subject_spans + rs_object_spans
            for span in spans:
                ana = span.attrs.get('data-dpt-ana')
                ref = span.attrs.get('data-dpt-ref').split(' ')
                content = span.get_text()
                in_relation_with = []
                is_object = False
                if len(ref) > 1:
                    # If ref contains more than one id, we extract all the ids in the
                    # ref attribute that are not the one of the character, and get the
                    # matching characters in database; if the first id is not the one of
                    # the character, it means it is an object in the annotation, not the subject
                    ref = [ int(id[1:]) for id in ref ]
                    if ref[0] != character.id:
                        is_object = True
                    ref = filter(lambda id: id != character.id, ref)
                    in_relation_with = [ Bonhum_StoryCharacter.objects.get(id=id) for id in ref ]
                ana = ana.split(' ')
                # We get the codes related to social relationships levels and types
                ana_levels = [ a for a in ana if a in social_levels.keys() ]
                ana_types = [ a for a in ana if a in social_types ]
                # We join the labels of the codes related to social relationships levels;
                # if the character is the object of the annotation, we get the inverse of each code
                if len(ana_levels) > 0:
                    if is_object:
                        level = ' ; '.join(map(lambda l: social_levels[social_levels_inverses[l]], ana_levels))
                    else:
                        level = ' ; '.join(map(lambda l: social_levels[l], ana_levels))
                else:
                    level = 'Unspecified'
                # For each code in the ana attribute, we add the related text segment
                # to our characteristics; we add the level or the relations if needed
                for code in ana:
                    # If the character is object and the code is for a familial relationship,
                    # we get the inverse code, according to the character gender if needed
                    if is_object and code in familial_inverses.keys():
                        if isinstance(familial_inverses[code], dict):
                            code = familial_inverses[code][character.gender.id] if character.gender else familial_inverses[code][1]
                        else:
                            code = familial_inverses[code]
                    # If the character is object and the code is for a
                    # social relationship level, we get the inverse code
                    if is_object and code in social_levels_inverses.keys():
                        code = social_levels_inverses[code]
                    # If the character is subject, we add the text segment for each code;
                    # if the character is object, we add it only if the code is for a relation
                    if not is_object or code[:12] == '#PROS-EV-REL':
                        data = { 'content': content, 'in_relation_with': in_relation_with }
                        if code in ana_types:
                            data['level'] = level
                        for category in characteristics:
                            if code in category['codes'].keys():
                                category['codes'][code]['annotations'].setdefault(tcx, []).append(data)
                                category['codes'][code]['nb'] += 1
                                category['nb'] += 1
                        # Special case: if the code is a social relationship level, and no type
                        # is specified, we also add the text segment to the type "Unspecified"
                        if code in ana_levels and len(ana_types) == 0:
                            characteristics[8]['codes']['#PROS-EV-REL-TY-SOC']['annotations'].setdefault(tcx, []).append({
                                'content': content, 'in_relation_with': in_relation_with, 'level': level
                            })
                            characteristics[8]['codes']['#PROS-EV-REL-TY-SOC']['nb'] += 1
                            characteristics[8]['nb'] += 1

        context['characteristics'] = characteristics

    def get_model(self):
        return Bonhum_StoryCharacter

    def get_form(self, request=None):
        initials = None
        if request:
            initials = request.GET
        return FilterCharacters(initials)

    @property
    def key(self):
        return 'characters'

    @property
    def label(self):
        return 'People'

    @property
    def label_singular(self):
        return 'Character'

    def _build_queryset_django(self, request, term):
        type = self.key
        query_characters = Bonhum_StoryCharacter.objects.filter(
                    Q(name__icontains=term) | \
                    Q(age__name__icontains=term) | \
                    Q(gender__name__icontains=term) | \
                    Q(religion__name__icontains=term) | \
                    Q(type__name__icontains=term) | \
                    Q(geographical_origin__name__icontains=term))

        name = request.GET.get('name', '')
        age = request.GET.get('age', '')
        gender = request.GET.get('gender', '')
        religion = request.GET.get('religion', '')
        type = request.GET.get('type', '')
        place = request.GET.get('place', '')

        self.is_advanced = name or age or gender or religion or type or place

        if name:
            query_characters = query_characters.filter(name=name)
        if age:
            query_characters = query_characters.filter(age__name=age)
        if gender:
            query_characters = query_characters.filter(gender__name=gender)
        if religion:
            query_characters = query_characters.filter(religion__name=religion)
        if type:
            query_characters = query_characters.filter(type__name=type)
        if place:
            query_characters = query_characters.filter(geographical_origin__name=place)

        self._queryset = query_characters.distinct().order_by('name')

        return self._queryset
