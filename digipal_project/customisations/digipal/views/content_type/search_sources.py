from django import forms
from digipal.views.content_type.search_content_type import SearchContentType, get_form_field_from_queryset
from digipal_text.models import TextContentXML
from digipal_project.models import Bonhum_Source, Bonhum_TextSource, Bonhum_Work
from django.forms.widgets import Select
from django.db.models import Q
from mezzanine.conf import settings
from digipal.utils import is_staff
from bs4 import BeautifulSoup
import re

def get_TE_buttons_info(category_id):
    TE_buttons = settings.TEXT_EDITOR_OPTIONS_CUSTOM['buttons']['btnSource']
    buttons = []
    category = next((category for category in TE_buttons['categories']
                    if category['id'] == category_id), None)
    if category:
        for item in category['items']:
            buttons.append({
                'code': item['attributes']['ana'],
                'label': item['label']
            })
    return buttons

class FilterSources(forms.Form):
    source_type = get_form_field_from_queryset(Bonhum_Source.objects.values_list('type__name', flat=True).order_by('type__name').distinct(), 'Type', aid='source_type')
    author = get_form_field_from_queryset(Bonhum_Source.objects.values_list('authors__name', flat=True).order_by('authors__name').distinct(), 'Author', aid='author')
    source_work = forms.ChoiceField(
        choices=[('', 'Work')] + [(work.title, work.title) for work in Bonhum_Work.objects.all()],
        widget=Select(attrs={'id': 'source_work', 'class': 'chzn-select',
        'data-placeholder': 'Choose a Work'}),
        label='', initial='Work', required=False
    )
    direct_typology = forms.ChoiceField(
        choices=[('', 'Typology (direct)')] + [(button['code'], button['label'])
                                               for button in get_TE_buttons_info('source_direct')],
        widget=Select(attrs={'id': 'direct_typology', 'class': 'chzn-select',
                             'data-placeholder': 'Choose a Typology'}),
        label='', initial='Typology (direct)', required=False
    )
    indirect_typology = forms.ChoiceField(
        choices=[('', 'Typology (indirect)')] + [(button['code'], button['label'])
                                               for button in get_TE_buttons_info('source_indirect')],
        widget=Select(attrs={'id': 'indirect_typology', 'class': 'chzn-select',
                             'data-placeholder': 'Choose a Typology'}),
        label='', initial='Typology (indirect)', required=False
    )

class SearchSources(SearchContentType):

    def get_fields_info(self):
        ''' See SearchContentType.get_fields_info() for a description of the field structure '''
        ret = super(SearchSources, self).get_fields_info()
        return ret

    def get_sort_fields(self):
        ''' returns a list of django field names necessary to sort the results '''
        return ['title']

    def get_headings(self):
        return [
            {'label': 'Title', 'key': 'title', 'is_sortable': True},
            {'label': 'Type', 'key': 'type', 'is_sortable': True}
        ]

    def set_record_view_context(self, context, request):
        super(SearchSources, self).set_record_view_context(context, request)
        source = Bonhum_Source.objects.get(id=context['id'])
        context['source'] = source

        # We get the buttons used to annotate sources in the texts
        TE_buttons = settings.TEXT_EDITOR_OPTIONS_CUSTOM['buttons']
        categories = TE_buttons['btnSource']['categories']
        items = [ item for category in categories for item in category['items'] ]

        text_content_xmls = TextContentXML.objects.all() if is_staff(request) else TextContentXML.get_public_only()
        text_content_xmls = text_content_xmls.filter(
                                text_content__text__id__in=source.texts.values_list('id')
                            )
        texts = []
        # For each text_content_xml linked to the source
        for tcx in text_content_xmls.filter(content__isnull=False):
            # We get the references of its links with the source
            references_in_db = Bonhum_TextSource.objects.filter(source__id=source.id).filter(text__id=tcx.text_content.text.id).values_list('canonical_reference', flat=True)
            soup = BeautifulSoup(tcx.content, 'lxml')
            # We get the <quote> annotations including the source id
            spans = soup.find_all('span', attrs={ 'data-dpt': 'quote',
                                                   'data-dpt-corresp': re.compile(ur'.*?#'
                                                   + str(source.id) + ur'\b.*?') })
            nb_annotations = 0
            annotations = {}
            for span in spans:
                url = tcx.get_absolute_url()
                url += '?' if ('?' not in url) else '&'
                url += 'annotation=%s' % span.attrs.get('data-dpt-id')
                content = span.get_text()
                ana = span.attrs.get('data-dpt-ana')
                label = filter(lambda item: item['attributes']['ana'] == ana, items)[0]['label']
                label += ' (direct)' if ana[:8] == '#SOUR-EV' else ' (indirect)'
                # We get all the references in the annotation
                n = str(span.attrs.get('data-dpt-n'))
                # We get the specific references concerning the source
                references_in_tcx = re.findall(source.reference + ur' \((.*?)\)|' + source.reference, n)[0]
                # If the source has been annotated without a reference,
                # we add the text segment with the key "No reference"
                if len(references_in_tcx) == 0:
                    annotations.setdefault('No reference', []).append({
                        'content': content, 'label': label, 'url': url
                    })
                    nb_annotations += 1
                # Else, we get each reference and add the related text segment
                else:
                    for reference in references_in_tcx.split(' ; '):
                        annotations.setdefault(reference, []).append({
                            'content': content, 'label': label, 'url': url
                        })
                        nb_annotations += 1
            # We check if there are references in the database that have not
            # been used to annotate, and we add them
            for reference in references_in_db:
                if len(reference) > 0 and reference not in annotations.keys():
                    annotations[reference] = []
            texts.append({
                'text_content_xml': tcx,
                'nb_annotations': nb_annotations,
                'annotations': annotations
            })

        context['texts'] = texts

    def get_model(self):
        return Bonhum_Source

    def get_form(self, request=None):
        initials = None
        if request:
            initials = request.GET
        return FilterSources(initials)

    @property
    def key(self):
        return 'sources'

    @property
    def label(self):
        return 'Sources'

    @property
    def label_singular(self):
        return 'Source'

    # Return ids of sources annotated with a specific code
    def get_ids_by_code(self, soup, code):
        # We get the <quote> annotations where the ana attribute is the code
        spans = soup.find_all('span', attrs={ 'data-dpt': 'quote', 'data-dpt-ana': code })
        ids = []
        # For each annotation, we get the ids of the related sources
        # (i.e. the ids in the corresp attribute)
        for span in spans:
            if span.attrs.get('data-dpt-corresp'):
                corresp = span.attrs.get('data-dpt-corresp').split(' ')
                ids += [ int(id[1:]) for id in corresp ]
        return ids

    def _build_queryset(self, request, term):
        type = self.key
        query_sources = Bonhum_Source.objects.filter(
            Q(title__icontains=term) | \
            Q(type__name__icontains=term) | \
            Q(authors__name__icontains=term)
        )

        source_type = request.GET.get('source_type', '')
        author = request.GET.get('author', '')
        source_work = request.GET.get('source_work', '')
        direct_typology_code = request.GET.get('direct_typology', '')
        indirect_typology_code = request.GET.get('indirect_typology', '')

        if source_type:
            query_sources = query_sources.filter(type__name=source_type)
        if author:
            query_sources = query_sources.filter(authors__name=author)
        if source_work:
            query_sources = query_sources.filter(
                Q(texts__edition__work__title=source_work) | \
                Q(texts__item_part__work_current_item__work__title=source_work)
            )

        tcx_contents = TextContentXML.objects.filter(content__isnull=False).values_list('content', flat=True)
        soup = BeautifulSoup(' '.join(tcx_contents), 'lxml')

        if direct_typology_code:
            query_sources = query_sources.filter(id__in=self.get_ids_by_code(soup, direct_typology_code))
        if indirect_typology_code:
            query_sources = query_sources.filter(id__in=self.get_ids_by_code(soup, indirect_typology_code))

        self._queryset = list(query_sources.distinct().order_by('title').values_list('id', flat=True))

        return self._queryset
