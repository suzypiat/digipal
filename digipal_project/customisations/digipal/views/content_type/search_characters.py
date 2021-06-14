from django import forms
from digipal.views.content_type.search_content_type import SearchContentType, get_form_field_from_queryset
from digipal.models import Image, Text
from digipal_text.models import TextContent, TextContentXML
from digipal_project.models import Bonhum_StoryCharacter
from django.db.models import Q

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

        images = Image.filter_permissions_from_request(Image.objects.filter(id__in=character.images.values_list('id')), request)
        context['images'] = Image.sort_query_set_by_locus(images)

        text_content_xmls = TextContentXML.objects.filter(text_content__text__id__in=character.texts.values_list('id'))
        context['text_content_xmls'] = text_content_xmls

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
