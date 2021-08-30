from django import forms
from digipal.views.content_type.search_content_type import SearchContentType, \
get_form_field_from_queryset
from digipal.models import Language
from digipal_text.models import TextContentXML
from digipal_project.models import Bonhum_Work
from django.forms.widgets import Select
from digipal.utils import is_staff
from django.db.models import Q
from mezzanine.conf import settings
from bs4 import BeautifulSoup
import re

def get_TE_buttons_info(btn_name, category_id=None):
    TE_buttons = settings.TEXT_EDITOR_OPTIONS_CUSTOM['buttons']
    if category_id:
        category = next((category for category in TE_buttons[btn_name]['categories']
                        if category['id'] == category_id), None)
        buttons = []
        if category:
            for item in category['items']:
                buttons.append({
                    'code': item['attributes']['ana'],
                    'label': item['label']
                })
    else:
        buttons = [ TE_buttons[button] for button in TE_buttons[btn_name]['buttons'] ]
        buttons = [ { 'code': button['ana'], 'label': button['label'] } for button in buttons ]
    return buttons

class FilterTexts(forms.Form):
    text_type = get_form_field_from_queryset(TextContentXML.objects.values_list('text_content__text__type__name', flat=True).order_by('text_content__text__type__name').distinct(), 'Type', aid='text_type')
    language = forms.ChoiceField(
        choices=[('', 'Language')] + [(language.name, language.name)
                 for language in Language.objects.all()],
        widget=Select(attrs={'id': 'language', 'class': 'chzn-select',
        'data-placeholder': 'Choose a Language'}),
        label='', initial='Language', required=False
    )
    text_work = forms.ChoiceField(
        choices=[('', 'Work')] + [(work.title, work.title)
                 for work in Bonhum_Work.objects.all()],
        widget=Select(attrs={'id': 'text_work', 'class': 'chzn-select',
        'data-placeholder': 'Choose a Work'}),
        label='', initial='Work', required=False
    )
    edition = get_form_field_from_queryset(TextContentXML.objects.values_list('text_content__text__edition__title', flat=True).order_by('text_content__text__edition__title').distinct(), 'Edition', aid='edition')
    item_part = get_form_field_from_queryset(TextContentXML.objects.values_list('text_content__text__item_part__display_label', flat=True).order_by('text_content__text__item_part__display_label').distinct(), 'Manuscript', aid='item_part')
    literary_function = forms.ChoiceField(
        choices=[('', 'Literary Function')] + [(button['code'], button['label'])
                                               for button in get_TE_buttons_info('btnLiteraryFunction')],
        widget=Select(attrs={'id': 'literary_function', 'class': 'chzn-select',
                             'data-placeholder': 'Choose a Literary Function'}),
        label='', initial='Literary Function', required=False,
    )
    target_gender = forms.ChoiceField(
        choices=[('', 'Aud. Gender')] + [(button['code'], button['label'])
                                      for button in get_TE_buttons_info('btnTargetAudience', 'target_audience_gender')],
        widget=Select(attrs={'id': 'target_gender', 'class': 'chzn-select',
                             'data-placeholder': 'Choose a Target Audience Gender'}),
        label='', initial='Aud. Gender', required=False
    )
    target_status = forms.ChoiceField(
        choices=[('', 'Aud. Social Status')] + [(button['code'], button['label'])
                                      for button in get_TE_buttons_info('btnTargetAudience', 'target_audience_social_status')],
        widget=Select(attrs={'id': 'target_status', 'class': 'chzn-select',
                             'data-placeholder': 'Choose a Target Audience Social Status'}),
        label='', initial='Aud. Social Status', required=False
    )
    target_function = forms.ChoiceField(
        choices=[('', 'Aud. Function')] + [(button['code'], button['label'])
                                      for button in get_TE_buttons_info('btnTargetAudience', 'target_audience_function')],
        widget=Select(attrs={'id': 'target_function', 'class': 'chzn-select',
                             'data-placeholder': 'Choose a Target Audience Function'}),
        label='', initial='Aud. Function', required=False
    )
    judgment = forms.ChoiceField(
        choices=[('', 'Judgment')] + [(button['code'], button['label'])
                                      for button in get_TE_buttons_info('btnJudgment')],
        widget=Select(attrs={'id': 'judgment', 'class': 'chzn-select',
                             'data-placeholder': 'Choose a Judgment'}),
        label='', initial='Judgment', required=False
    )
    date_type = forms.ChoiceField(
        choices=[('', 'Date')] + [(button['code'], button['label'])
                                      for button in get_TE_buttons_info('btnTime', 'date')],
        widget=Select(attrs={'id': 'date_type', 'class': 'chzn-select',
                             'data-placeholder': 'Choose a Date'}),
        label='', initial='Date', required=False
    )
    place_type = forms.ChoiceField(
        choices=[('', 'Place')] + [(button['code'], button['label'])
                                      for button in get_TE_buttons_info('btnPlace', 'place')],
        widget=Select(attrs={'id': 'place_type', 'class': 'chzn-select',
                             'data-placeholder': 'Choose a Place'}),
        label='', initial='Place', required=False
    )

class SearchTexts(SearchContentType):

    def get_fields_info(self):
        ''' See SearchContentType.get_fields_info() for a description of the field structure '''
        ret = super(SearchTexts, self).get_fields_info()
        return ret

    def get_sort_fields(self):
        ''' returns a list of django field names necessary to sort the results '''
        return ['text_content__text__title']

    def get_headings(self):
        return [
            {'label': 'Title', 'key': 'title', 'is_sortable': True},
            {'label': 'Type', 'key': 'type', 'is_sortable': True},
            {'label': 'Work', 'key': 'work', 'is_sortable': True}
        ]

    def get_model(self):
        return TextContentXML

    def get_form(self, request=None):
        initials = None
        if request:
            initials = request.GET
        return FilterTexts(initials)

    @property
    def key(self):
        return 'texts'

    @property
    def label(self):
        return 'Texts'

    @property
    def label_singular(self):
        return 'Text'

    # Return ids of texts containing at least one annotation with a specific code
    def get_ids_by_code(self, tag, code):
        tcxs = TextContentXML.objects.filter(content__isnull=False)
        ids = []
        for tcx in tcxs:
            soup = BeautifulSoup(tcx.content, 'lxml')
            # We check for an annotation including the code in the ana attribute
            span = soup.find('span', attrs={ 'data-dpt': tag, 'data-dpt-ana':
                                              re.compile(ur'.*?' + code + ur'\b.*?') })
            # If there is a matching span, we append the text id to the list of results
            if span:
                ids.append(tcx.id)
        return ids

    def _build_queryset(self, request, term):
        type = self.key
        query_texts = TextContentXML.objects.all() if is_staff(request) else TextContentXML.get_public_only()
        query_texts = query_texts.filter(
            Q(text_content__text__title__icontains=term) | \
            Q(text_content__text__type__name__icontains=term) | \
            Q(text_content__text__edition__title__icontains=term) | \
            Q(text_content__text__item_part__display_label__icontains=term) | \
            Q(text_content__text__edition__work__title__icontains=term) | \
            Q(text_content__text__item_part__work_current_item__work__title__icontains=term) | \
            # name of characters linked to the text
            Q(text_content__text__story_characters__name__icontains=term) | \
            # name variants of characters linked to the text
            Q(text_content__text__story_characters__bonhum_storycharacternamevariant__name__icontains=term) | \
            # title of sources linked to the text
            Q(text_content__text__sources__title__icontains=term) | \
            # name of authors of sources linked to the text
            Q(text_content__text__sources__authors__name__icontains=term)
        )

        text_type = request.GET.get('text_type', '')
        language = request.GET.get('language', '')
        text_work = request.GET.get('text_work', '')
        edition = request.GET.get('edition', '')
        item_part = request.GET.get('item_part', '')
        literary_function_code = request.GET.get('literary_function', '')
        target_gender_code = request.GET.get('target_gender', '')
        target_status_code = request.GET.get('target_status', '')
        target_function_code = request.GET.get('target_function', '')
        judgment_code = request.GET.get('judgment', '')
        date_code = request.GET.get('date_type', '')
        place_code = request.GET.get('place_type', '')

        if text_type:
            query_texts = query_texts.filter(text_content__text__type__name=text_type)
        if language:
            query_texts = query_texts.filter(
                Q(text_content__text__edition__work__language__name=language) | \
                Q(text_content__text__item_part__work_current_item__work__language__name=language)
            )
        if text_work:
            query_texts = query_texts.filter(
                Q(text_content__text__edition__work__title=text_work) | \
                Q(text_content__text__item_part__work_current_item__work__title=text_work)
            )
        if edition:
            query_texts = query_texts.filter(text_content__text__edition__title=edition)
        if item_part:
            query_texts = query_texts.filter(text_content__text__item_part__display_label=item_part)
        if literary_function_code:
            query_texts = query_texts.filter(id__in=self.get_ids_by_code('seg', literary_function_code))
        if target_gender_code:
            query_texts = query_texts.filter(id__in=self.get_ids_by_code('seg', target_gender_code))
        if target_status_code:
            query_texts = query_texts.filter(id__in=self.get_ids_by_code('seg', target_status_code))
        if target_function_code:
            query_texts = query_texts.filter(id__in=self.get_ids_by_code('seg', target_function_code))
        if judgment_code:
            query_texts = query_texts.filter(id__in=self.get_ids_by_code('seg', judgment_code))
        if date_code:
            query_texts = query_texts.filter(id__in=self.get_ids_by_code('date', date_code))
        if place_code:
            query_texts = query_texts.filter(id__in=self.get_ids_by_code('placeName', place_code))

        self._queryset = list(query_texts.distinct().order_by('text_content__text__title').values_list('id', flat=True))

        return self._queryset
