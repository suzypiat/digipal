from digipal.settings_docker import *

# Your custom project settings go here

INSTALLED_APPS = INSTALLED_APPS + ('digipal_project',)


# ITEM PART ADD FORM
USE_ITEM_PART_QUICK_ADD_FORM = False


# ADMIN DASHBOARD
ADMIN_MENU_ORDER = (
    ('Web Content',
        (
            'blog.BlogPost',
            'pages.Page',
            'digipal.CarouselItem',
            'generic.Keyword',
            'generic.ThreadedComment',
                (
                    'Media Library',
                    'fb_browse'
                )
        )
    ),
    ('Image',
        (
            'digipal.Image',
            'digipal.MediaPermission'
        )
    ),
    ('Text',
        (
            'digipal.Text',
            'digipal_project.Bonhum_TextType',
            'digipal_project.Bonhum_Work',
            'digipal_project.Bonhum_Edition',
            'digipal_project.Bonhum_Source',
            'digipal_project.Bonhum_SourceType',
            'digipal_project.Bonhum_Activity',
            'digipal_project.Bonhum_Collaborator',
            'digipal_text.TextContentXML',
            'digipal_text.TextContentType',
            'digipal_text.TextContentXMLStatus'
        )
    ),
    ('Item',
        (
            'digipal.HistoricalItem',
            'digipal.CurrentItem',
            'digipal.ItemPart',
            'digipal.HistoricalItemType',
        )
    ),
    ('Hand',
        (
            'digipal.Hand',
            'digipal.Scribe', # Contributors
            'digipal_project.Bonhum_ContributorType',
        )
    ),
    ('Annotation',
        (
            'digipal.Annotation',
            'digipal.Graph',
            'digipal.ImageAnnotationStatus'
        )
    ),
    ('Iconography',
        (
            'digipal.Ontograph', # Macro categories
            'digipal.OntographType', # Macro category types
            'digipal.Character', # Categories
            'digipal.CharacterForm', # Category forms
            'digipal.Allograph', # Motives
            'digipal.Idiograph', # Attributions
            'digipal.Language',
        )
    ),
    ('Descriptor',
        (
            'digipal.Component',
            'digipal.Feature',
            'digipal.ComponentFeature',
            'digipal.Aspect',
            'digipal.Appearance'
        )
    ),
    ('Actor',
        (
            'digipal.Person',
            'digipal.Repository',
            'digipal.Institution',
            'digipal.InstitutionType',
            'digipal.Place',
            'digipal.PlaceType'
        )
    ),
    ('Prosopography',
        (
            'digipal_project.Bonhum_StoryCharacter',
            'digipal_project.Bonhum_StoryPlace'
        )
    ),
    ('Prosopography Lists',
        (
            'digipal_project.Bonhum_StoryCharacterAge',
            'digipal_project.Bonhum_StoryCharacterGender',
            'digipal_project.Bonhum_StoryCharacterType',
            'digipal_project.Bonhum_StoryCharacterReligion',
            'digipal_project.Bonhum_StoryCharacterTitle',
            'digipal_project.Bonhum_StoryCharacterOccupation',
            'digipal_project.Bonhum_StoryCharacterTrait',
            'digipal_project.Bonhum_StoryPlaceNature',
            'digipal_project.Bonhum_StoryPlaceType'
        )
    ),
    ('Admin',
        (
            'auth.User',
            'auth.Group',
            'conf.Setting',
            'sites.Site',
            'redirects.Redirect',
            'digipal.RequestLog',
            'admin.LogEntry'
        )
    )
)


# MODELS EXPOSURE
MODELS_PRIVATE = ['itempart', 'image', 'graph', 'scribe', 'textcontentxml',
                  'bonhum_storycharacter', 'bonhum_source']
MODELS_PUBLIC = MODELS_PRIVATE


from digipal.views.faceted_search.settings import FACETED_SEARCH, FacettedType, get_fragment

# FACETED SEARCH: MANUSCRIPTS
manuscripts = FacettedType.fromKey('manuscripts')

# Change MS Date min and max
hi_date = manuscripts.getField('hi_date')
hi_date['min'] = 1330
hi_date['max'] = 1500

# Remove fields hi_index, hi_type, hi_format, hi_has_images
manuscripts.options['filter_order'] = ['hi_date', 'repo_place', 'repo_city']
manuscripts.options['column_order'] = ['url', 'repo_place', 'repo_city', 'shelfmark',
                                       'locus', 'hi_date', 'hi_image_count']

# FACETED SEARCH: IMAGES
images = FacettedType.fromKey('images')

# Change MS Date min and max
hi_date = images.getField('hi_date')
hi_date['min'] = 1330
hi_date['max'] = 1500

# Remove fields mp_permission, hi_type, hi_format
images.options['filter_order'] = ['hi_date', 'repo_place', 'repo_city']
images.options['column_order'] = ['url', 'repo_place', 'repo_city', 'shelfmark',
                                  'locus', 'hi_date', 'annotations', 'thumbnail']

# FACETED SEARCH: HANDS
hands = FacettedType.fromKey('hands')
hands.options['disabled'] = True

# FACETED SEARCH: SCRIBES (= PAINTERS)
scribes = FacettedType.fromKey('scribes')

# Label in Result Type section
scribes.options['label'] = 'Painter'

# Display painters only, not scribes
scribes.options['django_filter'] = {'type__name': 'Peintre'}

# Labels
scribe = scribes.getField('scribe')
scribe['label'] = 'Painter'

scriptorium = scribes.getField('scriptorium')
scriptorium['label'] = 'Workshop'

scribe_date = scribes.getField('scribe_date')
scribe_date['label'] = 'Date assigned to Painter'

# Change Date min and max
scribe_date['min'] = 1330
scribe_date['max'] = 1500

def filter_empty(result):
    if result and len(result) > 0:
        if isinstance(result, list):
            result = filter(None, result)
            if len(result) == 0:
                return
        return result

# Add Repository
repo_place = {
    'key': 'repo_place', 'label': 'Repository',
    'path': 'hands.all.item_part.work_current_item.current_item.repository.human_readable',
    'path_result': 'hands.all.item_part.work_current_item.current_item.repository.name',
    'transform': filter_empty,
    'count': True, 'search': True, 'viewable': True, 'type': 'title', 'multivalued': True
}
scribes.addField(repo_place)

# Add Repository City
repo_city = {
    'key': 'repo_city', 'label': 'Repository City',
    'path': 'hands.all.item_part.work_current_item.current_item.repository.place.name',
    'transform': filter_empty,
    'count': True, 'search': True, 'viewable': True, 'type': 'title', 'multivalued': True
}
scribes.addField(repo_city)

# Add Shelfmark
shelfmark = {
    'key': 'shelfmark', 'label': 'Shelfmark',
    'path': 'hands.all.item_part.work_current_item.current_item.shelfmark',
    'transform': filter_empty,
    'search': True, 'viewable': True, 'type': 'code', 'multivalued': True
}
scribes.addField(shelfmark)

# Add MS Date
hi_date = {
    'key': 'hi_date', 'label': 'MS Date',
    'path': 'hands.all.item_part.historical_item.get_date_sort',
    'transform': filter_empty,
    'search': True, 'viewable': True, 'type': 'date', 'multivalued': True
}
scribes.addField(hi_date)

# Add fields repo_place, repo_city, shelfmark, hi_date
scribes.options['filter_order'] = ['scribe_date', 'scriptorium', 'repo_place', 'repo_city']
scribes.options['column_order'] = ['url', 'scribe', 'scribe_date', 'scriptorium',
                                   'repo_place', 'repo_city', 'shelfmark', 'hi_date']

# FACETED SEARCH: TEXTS
texts = FacettedType.fromKey('texts')

# Add Title
title = {
    'key': 'title', 'label': 'Title',
    'path': 'text_content.text.title',
    'viewable': True, 'type': 'title', 'search': True
}
texts.addField(title)

# Add Edition
edition = {
    'key': 'edition', 'label': 'Edition',
    'path': 'text_content.text.edition.title',
    'viewable': True, 'type': 'title', 'count': True, 'search': True
}
texts.addField(edition)

# Add Work
def get_text_work(text):
    if text and text.item_part:
        return text.item_part.work_current_item.work.title
    elif text and text.edition:
        return text.edition.work.title

work = {
    'key': 'work', 'label': 'Work',
    'path': 'text_content.text', 'transform': get_text_work,
    'viewable': True, 'type': 'title', 'count': True, 'search': True
}
texts.addField(work)

# Add Language
def get_text_language(text):
    if text and text.item_part:
        return text.item_part.work_current_item.work.language.name
    elif text and text.edition:
        return text.edition.work.language.name

language = {
    'key': 'language', 'label': 'Language',
    'path': 'text_content.text', 'transform': get_text_language,
    'viewable': True, 'type': 'title', 'count': True, 'search': True
}
texts.addField(language)

# Change path for Text Type
text_type = texts.getField('text_type')
text_type['path'] = 'text_content.text.type.name'

# Change path for Thumbnail
# (if the text comes from an item part, it is the first image linked to this item part;
# if the text comes from an edition, it is the first image linked to the text)
def get_text_thumbnail(text):
    if text and text.item_part:
        return text.item_part.get_first_image()
    elif text and text.edition:
        return text.get_first_image()

thumbnail = texts.getField('thumbnail')
thumbnail['path'] = 'text_content.text'
thumbnail['transform'] = get_text_thumbnail

# Remove fields hi_type, repo_city
# Add fields title, work, edition, language
texts.options['filter_order'] = ['work', 'language','text_type', 'repo_place']
texts.options['column_order'] = ['url', 'title', 'language', 'text_type', 'edition', 'work',
                                 'hi_date', 'shelfmark', 'repo_place', 'thumbnail']

# FACETED SEARCH: GRAPHS (= ICONOGRAPHY)
graphs = FacettedType.fromKey('graphs')

# Label in Result Type section
graphs.options['label'] = 'Iconography'
graphs.options['label_plural'] = 'Iconography'

# Labels
allograph = graphs.getField('allograph')
allograph['label'] = 'Motive'

character = graphs.getField('character')
character['label'] = 'Category'

# Add Macro Category
ontograph = {
    'key': 'ontograph', 'label': 'Macro Category',
    'path': 'idiograph.allograph.character.ontograph.name',
    'viewable': True, 'type': 'id', 'count': True, 'search': True
}
graphs.addField(ontograph)

# Add Motive (motive without a story character)
def get_graph_generic_motive(allograph):
    if allograph and not hasattr(allograph, 'bonhum_motivestorycharacter'):
        return allograph.name

generic_motive = {
    'key': 'generic_motive', 'label': 'Motive',
    'path': 'idiograph.allograph', 'transform': get_graph_generic_motive,
    'viewable': True, 'type': 'id', 'count': True, 'search': True
}
graphs.addField(generic_motive)

# Add Character Motive (motive with a story character)
def get_graph_story_character_motive(allograph):
    if allograph and hasattr(allograph, 'bonhum_motivestorycharacter'):
        return allograph.bonhum_motivestorycharacter.name

story_character_motive = {
    'key': 'story_character_motive', 'label': 'Character Motive',
    'path': 'idiograph.allograph', 'transform': get_graph_story_character_motive,
    'viewable': True, 'type': 'id', 'count': True, 'search': True
}
graphs.addField(story_character_motive)

# Remove fields hand_label, hand_date, hand_place, is_described, chartype, character_form
# Add fields ontograph, generic_motive, story_character_motive
graphs.options['filter_order'] = ['ontograph', 'character', 'generic_motive',
                                  'story_character_motive', 'repo_place', 'repo_city']
graphs.options['column_order'] = ['url', 'repo_place', 'repo_city', 'shelfmark',
                                  'locus', 'hi_date', 'allograph', 'thumbnail']

# FACETED SEARCH: PEOPLE
FACETED_SEARCH['types'].append({
    'disabled': False,
    'key': 'characters',
    'label': 'Character',
    'label_plural': 'People',
    'model': 'digipal_project.models.Bonhum_StoryCharacter',
    'fields': [
        {'key': 'url', 'label': 'Address', 'label_col': ' ',
         'path': 'get_absolute_url',
         'type': 'url', 'viewable': True},

        {'key': 'name', 'label': 'Name',
         'path': 'name',
         'type': 'title', 'viewable': True, 'search': True},

        {'key': 'variants', 'label': 'Alias',
         'path': 'bonhum_storycharacternamevariant_set.all.name',
         'type': 'title', 'viewable': True, 'search': True, 'multivalued': True},

        {'key': 'titles', 'label': 'Titles',
         'path': 'titles.all.name',
         'type': 'title', 'viewable': True, 'search': True, 'multivalued': True},

        {'key': 'occupations', 'label': 'Professions',
         'path': 'occupations.all.name',
         'type': 'title', 'viewable': True, 'search': True, 'multivalued': True},

        {'key': 'traits', 'label': 'Traits',
         'path': 'traits.all.name',
         'type': 'title', 'viewable': True, 'search': True, 'multivalued': True},

        {'key': 'type', 'label': 'Type',
         'path': 'type.name',
         'type': 'title', 'viewable': True, 'search': True, 'count': True},

        {'key': 'age', 'label': 'Age',
         'path': 'age.name',
         'type': 'title', 'viewable': True, 'search': True, 'count': True},

        {'key': 'gender', 'label': 'Gender',
         'path': 'gender.name',
         'type': 'title', 'viewable': True, 'search': True, 'count': True},

        {'key': 'religion', 'label': 'Religion',
         'path': 'religion.name',
         'type': 'title', 'viewable': True, 'search': True, 'count': True},

        {'key': 'place', 'label': 'Place',
         'path': 'geographical_origin.name',
         'type': 'title', 'viewable': True, 'search': True, 'count': True},

        {'key': 'texts', 'label': 'Texts',
         'path': 'texts.all.title',
         'type': 'title', 'viewable': True, 'search': True, 'multivalued': True},

        {'key': 'thumbnail', 'label': 'Thumbnail',
         'path': 'get_thumbnail',
         'viewable': True, 'type': 'image'}
    ],
    'filter_order': ['type', 'age', 'gender', 'religion', 'place'],
    'column_order': ['url', 'name', 'variants', 'titles', 'occupations', 'traits',
                     'type', 'place', 'texts', 'thumbnail']
})

# FACETED SEARCH: SOURCES
def get_source_work(result):
    if result:
        # result is a single text
        if not isinstance(result, list):
            if result.edition:
                return result.edition.work.title
            elif result.item_part:
                return result.item_part.work_current_item.work.title
        # result is a list of works
        return result

def get_source_grid_authors():
    from digipal_project.models import Bonhum_Source
    from digipal.models import Person
    authors = []
    authors_ids = filter(None, Bonhum_Source.objects.values_list('authors', flat=True))
    for id in authors_ids:
        author = Person.objects.get(id=id)
        if author not in authors:
            authors.append(author)
    authors = sorted(authors, key=lambda author: author.name)
    return authors

def get_source_grid_works():
    from digipal_project.models import Bonhum_Source, Bonhum_Work
    works = Bonhum_Work.objects.all()
    ret = {}
    for work in works:
        ret[work.title] = []
    sources = Bonhum_Source.objects.all()
    for source in sources:
        for text in source.texts.all():
            if text.edition:
                work = text.edition.work
            elif text.item_part:
                work = text.item_part.work_current_item.work
            if source not in ret[work.title]:
                ret[work.title].append(source)
    ret = { work_title: sources for work_title, sources in ret.items() if len(sources) > 0 }
    return ret

FACETED_SEARCH['types'].append({
    'disabled': False,
    'key': 'sources',
    'label': 'Source',
    'model': 'digipal_project.models.Bonhum_Source',
    'fields': [
        {'key': 'url', 'label': 'Address', 'label_col': ' ',
         'path': 'get_absolute_url',
         'type': 'url', 'viewable': True},

        {'key': 'title', 'label': 'Title',
         'path': 'title',
         'type': 'title', 'viewable': True, 'search': True},

        {'key': 'authors', 'label': 'Authors',
         'path': 'authors.all.name',
         'type': 'title', 'viewable': True, 'search': True, 'multivalued': True},

        {'key': 'type', 'label': 'Type',
         'path': 'type.name',
         'type': 'title', 'viewable': True, 'search': True, 'count': True},

        {'key': 'texts', 'label': 'Texts',
         'path': 'texts.all.title',
         'type': 'title', 'viewable': True, 'search': True, 'multivalued': True},

        {'key': 'work', 'label': 'Work',
         'path': 'texts.all',
         'transform': get_source_work,
         'type': 'title', 'viewable': True, 'search': True, 'count': True, 'multivalued': True}
    ],
    'filter_order': ['type', 'work'],
    'column_order': ['url', 'title', 'authors', 'type', 'work', 'texts'],
    'views': [
        get_fragment('view_default'),
        {'icon': 'list-alt', 'label': 'Grouped Grid View', 'key': 'ggrid',
         'type': 'ggrid', 'template': 'source_grid_grouped',
         'params': {'authors': get_source_grid_authors, 'works': get_source_grid_works}}
    ]
})


# TEXT_EDITOR
TE_COLOR_LITERARY_FUNCTION = '#c5e0b3'
TE_COLOR_TARGET_AUDIENCE = '#a8d08d'
TE_COLOR_JUDGMENT = '#538135'
TE_COLOR_DIRECT_SOURCE = '#f7caac'
TE_COLOR_INDIRECT_SOURCE = '#f4b083'
TE_COLOR_PLACE = '#ffe599'
TE_COLOR_TIME = '#d9d9d9'
TE_COLOR_PERSON_NAME = '#b4c6e7'
TE_COLOR_PERSON = '#8eaadb'

TEXT_EDITOR_OPTIONS_CUSTOM = {
    'buttons': {

        # Literary Function
        'btnConsolationLiteraryFunction': { 'label': 'Consolation', 'tei': '<seg ana="#LIT-FON-CONS">{}</seg>', 'color': TE_COLOR_LITERARY_FUNCTION },
        'btnSelfAwarenessLiteraryFunction': { 'label': 'Self Awareness', 'tei': '<seg ana="#LIT-FON-CONN-SOI">{}</seg>', 'color': TE_COLOR_LITERARY_FUNCTION },
        'btnWorldKnowledgeLiteraryFunction': { 'label': 'World Knowledge', 'tei': '<seg ana="#LIT-FON-CONN-MON">{}</seg>', 'color': TE_COLOR_LITERARY_FUNCTION },
        'btnEntertainmentLiteraryFunction': { 'label': 'Entertainment', 'tei': '<seg ana="#LIT-FON-DIV">{}</seg>', 'color': TE_COLOR_LITERARY_FUNCTION },
        'btnThaumaturgicLiteraryFunction': { 'label': 'Thaumaturgic', 'tei': '<seg ana="#LIT-FON-THAUM">{}</seg>', 'color': TE_COLOR_LITERARY_FUNCTION },
        'btnMetaLiteraryLiteraryFunction': { 'label': 'Metaliterary', 'tei': '<seg ana="#LIT-FON-META">{}</seg>', 'color': TE_COLOR_LITERARY_FUNCTION },
        'btnCivicFunctionLiteraryFunction': { 'label': 'Civic Function', 'tei': '<seg ana="#LIT-FON-SOCIOPOL-CIV">{}</seg>', 'color': TE_COLOR_LITERARY_FUNCTION },
        'btnInterpersonalLiteraryFunction': { 'label': 'Interpersonal', 'tei': '<seg ana="#LIT-FON-SOCIOPOL-INTERPERS">{}</seg>', 'color': TE_COLOR_LITERARY_FUNCTION },

        'btnLiteraryFunction': { 'label': 'Literary Function', 'buttons': [
            'btnConsolationLiteraryFunction', 'btnSelfAwarenessLiteraryFunction',
            'btnWorldKnowledgeLiteraryFunction', 'btnEntertainmentLiteraryFunction',
            'btnThaumaturgicLiteraryFunction', 'btnMetaLiteraryLiteraryFunction',
            'btnCivicFunctionLiteraryFunction', 'btnInterpersonalLiteraryFunction'
        ]},

        # Target Audience
        'btnTargetAudience': {
            'label': 'Target Audience',
            'tei': '<seg>{}</seg>',
            'triggerName': 'onClickBtnTargetAudience',
            'color': TE_COLOR_TARGET_AUDIENCE,
            'categories': [
                {
                    'label': 'Gender',
                    'items': [
                        {
                            'id': 'btnMaleGenderTargetAudience', 'label': 'Male', 'color': TE_COLOR_TARGET_AUDIENCE,
                            'tag': 'seg', 'attributes': { 'ana': '#LIT-PUBL-GEN-M' }
                        },
                        {
                            'id': 'btnFemaleGenderTargetAudience', 'label': 'Female', 'color': TE_COLOR_TARGET_AUDIENCE,
                            'tag': 'seg', 'attributes': { 'ana': '#LIT-PUBL-GEN-F' }
                        }
                    ]
                },
                {
                    'label': 'Social Status',
                    'items': [
                        {
                            'id': 'btnHighSocialStatusTargetAudience', 'label': 'High', 'color': TE_COLOR_TARGET_AUDIENCE,
                            'tag': 'seg', 'attributes': { 'ana': '#LIT-PUBL-NSOC-H' }
                        },
                        {
                            'id': 'btnLowSocialStatusTargetAudience', 'label': 'Low', 'color': TE_COLOR_TARGET_AUDIENCE,
                            'tag': 'seg', 'attributes': { 'ana': '#LIT-PUBL-NSOC-B' }
                        }
                    ]
                },
                {
                    'label': 'Function',
                    'items': [
                        {
                            'id': 'btnExegeticFunctionTargetAudience', 'label': 'Exegetic', 'color': TE_COLOR_TARGET_AUDIENCE,
                            'tag': 'seg', 'attributes': { 'ana': '#LIT-PUBL-FON-EXE' }
                        },
                        {
                            'id': 'btnDidacticFunctionTargetAudience', 'label': 'Didactic', 'color': TE_COLOR_TARGET_AUDIENCE,
                            'tag': 'seg', 'attributes': { 'ana': '#LIT-PUBL-FON-DID' }
                        }
                    ]
                }
            ]
        },

        # Judgment
        'btnAmbiguousJudgment': { 'label': 'Ambiguous', 'tei': '<seg ana="#BOC-A">{}</seg>', 'color': TE_COLOR_JUDGMENT },
        'btnPositiveJudgment': { 'label': 'Positive', 'tei': '<seg ana="#BOC-P">{}</seg>', 'color': TE_COLOR_JUDGMENT },
        'btnNegativeJudgment': { 'label': 'Negative', 'tei': '<seg ana="#BOC-N">{}</seg>', 'color': TE_COLOR_JUDGMENT },
        'btnNeutralJudgment': { 'label': 'Neutral', 'tei': '<seg ana="#BOC-NEU">{}</seg>', 'color': TE_COLOR_JUDGMENT },
        'btnIronicJudgment': { 'label': 'Ironic', 'tei': '<seg ana="#BOC-IRO">{}</seg>', 'color': TE_COLOR_JUDGMENT },

        'btnJudgment': { 'label': 'Judgment', 'buttons': [
            'btnAmbiguousJudgment', 'btnPositiveJudgment', 'btnNegativeJudgment',
            'btnNeutralJudgment', 'btnIronicJudgment'
        ]},

        # Source
        'btnSource': {
            'label': 'Source',
            'tei': '<quote>{}</quote>',
            'triggerName': 'onClickBtnSource',
            'categories': [
                {
                    'label': 'Direct Source',
                    'items': [
                        {
                            'id': 'btnLexicalDirectSource', 'label': 'Lexical', 'color': TE_COLOR_DIRECT_SOURCE,
                            'tag': 'quote', 'attributes': { 'corresp': '#ID_SOURCE', 'ana': '#SOUR-EV-LEX', 'n': 'REFERENCE_SOURCE' }
                        },
                        {
                            'id': 'btnContentDirectSource', 'label': 'Content', 'color': TE_COLOR_DIRECT_SOURCE,
                            'tag': 'quote', 'attributes': { 'corresp': '#ID_SOURCE', 'ana': '#SOUR-EV-CONT', 'n': 'REFERENCE_SOURCE' }
                        },
                        {
                            'id': 'btnAuthorNameDirectSource', 'label': 'Author Name', 'color': TE_COLOR_DIRECT_SOURCE,
                            'tag': 'quote', 'attributes': { 'corresp': '#ID_SOURCE', 'ana': '#SOUR-EV-AUT', 'n': 'REFERENCE_SOURCE' }
                        },
                        {
                            'id': 'btnTitleDirectSource', 'label': 'Title', 'color': TE_COLOR_DIRECT_SOURCE,
                            'tag': 'quote', 'attributes': { 'corresp': '#ID_SOURCE', 'ana': '#SOUR-EV-TIT', 'n': 'REFERENCE_SOURCE' }
                        },
                        {
                            'id': 'btnAuthorNameAndTitleDirectSource', 'label': 'Author Name and Title', 'color': TE_COLOR_DIRECT_SOURCE,
                            'tag': 'quote', 'attributes': { 'corresp': '#ID_SOURCE', 'ana': '#SOUR-EV-AUT-TIT', 'n': 'REFERENCE_SOURCE' }
                        }
                    ]
                },
                {
                    'label': 'Indirect Source',
                    'items': [
                        {
                            'id': 'btnLexicalIndirectSource', 'label': 'Lexical', 'color': TE_COLOR_INDIRECT_SOURCE,
                            'tag': 'quote', 'attributes': { 'corresp': '#ID_SOURCE', 'ana': '#SOUR-IND-LEX', 'n': 'REFERENCE_SOURCE' }
                        },
                        {
                            'id': 'btnContentIndirectSource', 'label': 'Content', 'color': TE_COLOR_INDIRECT_SOURCE,
                            'tag': 'quote', 'attributes': { 'corresp': '#ID_SOURCE', 'ana': '#SOUR-IND-CONT', 'n': 'REFERENCE_SOURCE' }
                        },
                        {
                            'id': 'btnAuthorNameIndirectSource', 'label': 'Author Name', 'color': TE_COLOR_INDIRECT_SOURCE,
                            'tag': 'quote', 'attributes': { 'corresp': '#ID_SOURCE', 'ana': '#SOUR-IND-AUT', 'n': 'REFERENCE_SOURCE' }
                        },
                        {
                            'id': 'btnTitleIndirectSource', 'label': 'Title', 'color': TE_COLOR_INDIRECT_SOURCE,
                            'tag': 'quote', 'attributes': { 'corresp': '#ID_SOURCE', 'ana': '#SOUR-IND-TIT', 'n': 'REFERENCE_SOURCE' }
                        },
                        {
                            'id': 'btnAuthorNameAndTitleIndirectSource', 'label': 'Author Name and Title', 'color': TE_COLOR_INDIRECT_SOURCE,
                            'tag': 'quote', 'attributes': { 'corresp': '#ID_SOURCE', 'ana': '#SOUR-IND-AUT-TIT', 'n': 'REFERENCE_SOURCE' }
                        }
                    ]
                }
            ]
        },

        # Place
        'btnPlace': {
            'label': 'Place',
            'tei': '<placeName>{}</placeName>',
            'triggerName': 'onClickBtnPlace',
            'categories': [
                {
                    'label': '',
                    'items': [
                        {
                            'id': 'btnCityPlace', 'label': 'City', 'color': TE_COLOR_PLACE,
                            'tag': 'placeName', 'attributes': { 'ref': '#ID_PLACE #ID_PERSON', 'ana': '#PROS-L-VIL' }
                        },
                        {
                            'id': 'btnCountryPlace', 'label': 'Country', 'color': TE_COLOR_PLACE,
                            'tag': 'placeName', 'attributes': { 'ref': '#ID_PLACE #ID_PERSON', 'ana': '#PROS-L-PAY' }
                        },
                        {
                            'id': 'btnContinentPlace', 'label': 'Continent', 'color': TE_COLOR_PLACE,
                            'tag': 'placeName', 'attributes': { 'ref': '#ID_PLACE #ID_PERSON', 'ana': '#PROS-L-CONT' }
                        }
                    ]
                }
            ]
        },

        # Time
        'btnTime': {
            'label': 'Time',
            'tei': '<date>{}</date>',
            'triggerName': 'onClickBtnTime',
            'categories': [
                {
                    'label': '',
                    'items': [
                        {
                            'id': 'btnRealTime', 'label': 'Real', 'color': TE_COLOR_TIME,
                            'tag': 'date', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-CR-TR' }
                        },
                        {
                            'id': 'btnMythologicalTime', 'label': 'Mythological', 'color': TE_COLOR_TIME,
                            'tag': 'date', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-CR-TM' }
                        }
                    ]
                }
            ]
        },

        # Person
        'btnPerson': {
            'label': 'Person',
            'tei': '<rs>{}</rs>',
            'triggerName': 'onClickBtnPerson',
            'color': TE_COLOR_PERSON,
            'categories': [
                {
                    'label': 'Person Name',
                    'items': [
                        {
                            'id': 'btnPersonName', 'label': 'Person Name', 'color': TE_COLOR_PERSON_NAME,
                            'tag': 'persName', 'attributes': { 'ref': '#ID_PERSON' }
                        }
                    ]
                },
                {
                    'label': 'Status',
                    'items': [
                        {
                            'id': 'btnSingleStatusPerson', 'label': 'Single', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-ST-C' }
                        },
                        {
                            'id': 'btnMarriedStatusPerson', 'label': 'Married', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-ST-M' }
                        },
                        {
                            'id': 'btnWidowedStatusPerson', 'label': 'Widower/Widow', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-ST-V' }
                        }
                    ]
                },
                {
                    'label': 'Physical Aspect',
                    'items': [
                        {
                            'id': 'btnPhysicalAspectPerson', 'label': 'Physical Aspect', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-PHY' }
                        }
                    ]
                },
                {
                    'label': 'Psychology',
                    'items': [
                        {
                            'id': 'btnHappinessPsychologyPerson', 'label': 'Happiness', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-PSY-BON' }
                        },
                        {
                            'id': 'btnUnhappinessPsychologyPerson', 'label': 'Unhappiness', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-PSY-MAL' }
                         }
                    ]
                },
                {
                    'label': 'Socio Economic Status',
                    'items': [
                        {
                            'id': 'btnStatusSocioEconomicStatusPerson', 'label': 'Status', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-NSOCIO-EC-S' }
                        },
                        {
                            'id': 'btnAscensionSocioEconomicStatusPerson', 'label': 'Ascension', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-NSOCIO-EC-S-A' }
                        },
                        {
                            'id': 'btnDeclineSocioEconomicStatusPerson', 'label': 'Decline', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-NSOCIO-EC-S-D' }
                        },
                        {
                            'id': 'btnClothesSocioEconomicStatusPerson', 'label': 'Clothes', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-NSOCIO-EC-HAB' }
                        },
                        {
                            'id': 'btnBuildingEstateSocioEconomicStatusPerson', 'label': 'Building Estate', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-NSOCIO-EC-HABIT' }
                        },
                        {
                            'id': 'btnPropertiesSocioEconomicStatusPerson', 'label': 'Properties', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-NSOCIO-EC-PROPR' }
                        }
                    ]
                },
                {
                    'label': 'Culture',
                    'items': [
                        {
                            'id': 'btnHighCulturePerson', 'label': 'High Level of Language', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-CUL-NLANG-H' }
                        },
                        {
                            'id': 'btnLowCulturePerson', 'label': 'Low Level of Language', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-CUL-NLANG-B' }
                        }
                    ]
                },
                {
                    'label': 'Relation With',
                    'items': [
                        {
                            'id': 'btnRelationWithPerson', 'label': 'Relation With', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON #ID_PERSON_WITH', 'ana': '#PROS-EV-REL-AVEC' }
                        }
                    ]
                },
                {
                    'label': 'Family Relationship',
                    'items': [
                        {
                            'id': 'btnFamilyRelationPerson', 'label': 'Unspecified', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-FAM' }
                        },
                        {
                            'id': 'btnChildFamilyRelationPerson', 'label': 'Child', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-FAM-ENF' }
                        },
                        {
                            'id': 'btnGrandchildFamilyRelationPerson', 'label': 'Grandchild', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-FAM-PTSENF' }
                        },
                        {
                            'id': 'btnParentFamilyRelationPerson', 'label': 'Parent', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-FAM-PAR' }
                        },
                        {
                            'id': 'btnGrandparentFamilyRelationPerson', 'label': 'Grandparent', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-FAM-GRPAR' }
                        },
                        {
                            'id': 'btnUncleFamilyRelationPerson', 'label': 'Uncle', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-FAM-ONC' }
                        },
                        {
                            'id': 'btnAuntFamilyRelationPerson', 'label': 'Aunt', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-FAM-TAN' }
                        },
                        {
                            'id': 'btnNephewFamilyRelationPerson', 'label': 'Nephew', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-FAM-NEV' }
                        },
                        {
                            'id': 'btnNieceFamilyRelationPerson', 'label': 'Niece', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-FAM-NIEC' }
                        },
                        {
                            'id': 'btnSiblingFamilyRelationPerson', 'label': 'Sibling', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-FAM-FRA' }
                        },
                        {
                            'id': 'btnMarriageFamilyRelationPerson', 'label': 'Marriage', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-FAM-MAR' }
                        },
                        {
                            'id': 'btnGodparentFamilyRelationPerson', 'label': 'Godparent', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-FAM-PARR' }
                        }
                    ]
                },
                {
                    'label': 'Social Relationship',
                    'items': [
                        {
                            'id': 'btnSocialRelationPerson', 'label': 'Unspecified', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-SOC' }
                        },
                        {
                            'id': 'btnProfessionalSocialRelationPerson', 'label': 'Professional', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-SOC-TY-PRO' }
                        },
                        {
                            'id': 'btnInstitutionalSocialRelationPerson', 'label': 'Institutional', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-SOC-TY-INST' }
                        },
                        {
                            'id': 'btnLoveSocialRelationPerson', 'label': 'Love', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-SOC-TY-AMOR' }
                        },
                        {
                            'id': 'btnFriendshipSocialRelationPerson', 'label': 'Friendship', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-SOC-TY-AMIC' }
                        },
                        {
                            'id': 'btnHostilitySocialRelationPerson', 'label': 'Hostility', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-SOC-TY-HOST' }
                        },
                        {
                            'id': 'btnInferiorSocialRelationPerson', 'label': 'With an inferior', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-SOC-N-AVECI' }
                        },
                        {
                            'id': 'btnSuperiorSocialRelationPerson', 'label': 'With a superior', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-SOC-N-AVECS' }
                        },
                        {
                            'id': 'btnEqualSocialRelationPerson', 'label': 'With an equal', 'color': TE_COLOR_PERSON,
                            'tag': 'rs', 'attributes': { 'ref': '#ID_PERSON', 'ana': '#PROS-EV-REL-TY-SOC-N-AVECP' }
                        }
                    ]
                }
            ]
        }
    },
    'toolbars': {
        'default': 'psclear undo redo pssave | psconvert | btnLiteraryFunction | btnTargetAudience | btnPerson | pslocation | btnTime | btnPlace | btnSource | btnJudgment | code ',
        'edited': 'psclear undo redo pssave | psconvert | btnLiteraryFunction | btnTargetAudience | btnPerson | btnTime | btnPlace | btnSource | btnJudgment | code ',
    },
    'panels': {
        'north': {
            'ratio': 0.0
        },
        'east': {
            'ratio': 0.5
        }
    },
    'show_highlights_in_preview': 0
}
