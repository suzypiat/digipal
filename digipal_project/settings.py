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
MODELS_PRIVATE = ['itempart', 'image', 'graph', 'scribe', 'textcontentxml', 'bonhum_storycharacter']
MODELS_PUBLIC = MODELS_PRIVATE


from digipal.views.faceted_search.settings import FACETED_SEARCH, FacettedType

# FACETED SEARCH: MANUSCRIPTS
manuscripts = FacettedType.fromKey('manuscripts')

# Remove fields hi_type, hi_format, hi_has_images
manuscripts.options['filter_order'] = ['hi_date', 'repo_city', 'repo_place']
manuscripts.options['column_order'] = ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_index', 'hi_date', 'hi_image_count']

# FACETED SEARCH: IMAGES
images = FacettedType.fromKey('images')

# Remove fields mp_permission, hi_type, hi_format
images.options['filter_order'] = ['hi_date', 'repo_city', 'repo_place']
images.options['column_order'] = ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date', 'annotations', 'thumbnail']

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

scribe_date = scribes.getField('scribe_date')
scribe_date['label'] = 'Date assigned to Painter'

scriptorium = scribes.getField('scriptorium')
scriptorium['label'] = 'Workshop'

# Add Repository
repo_place = {
    'key': 'repo_place', 'label': 'Repository',
    'path': 'hands.all.item_part.current_item.repository.human_readable',
    'path_result': 'hands.all.item_part.current_item.repository.name',
    'count': True, 'search': True, 'viewable': True, 'type': 'title', 'multivalued': True
}
scribes.addField(repo_place)

# Add Repository City
repo_city = {
    'key': 'repo_city', 'label': 'Repository City',
    'path': 'hands.all.item_part.current_item.repository.place.name',
    'count': True, 'search': True, 'viewable': True, 'type': 'title', 'multivalued': True
}
scribes.addField(repo_city)

# Add fields repo_place, repo_city
scribes.options['filter_order'] = ['scribe_date', 'scriptorium', 'repo_place', 'repo_city']
scribes.options['column_order'] = ['url', 'scribe', 'scribe_date', 'scriptorium']

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
    'path': 'text_content.edition.title',
    'viewable': True, 'type': 'title', 'count': True, 'search': True
}
texts.addField(edition)

# Add Languages
languages = {
    'key': 'languages', 'label': 'Languages',
    'path': 'text_content.languages.all.name',
    'viewable': True, 'type': 'title', 'count': True, 'search': True, 'multivalued': True
}
texts.addField(languages)

# Change path for Text Type
text_type = texts.getField('text_type')
text_type['path'] = 'text_content.text.type.name'

# Change path for Thumbnail
# (if the text comes from an item part, it is the first image linked to this item part;
# if the text comes from an edition, it is the first image linked to the text)
def get_thumbnail(text):
    if text and text.item_part:
        return text.item_part.get_first_image()
    elif text and text.edition:
        return text.get_first_image()

thumbnail = texts.getField('thumbnail')
thumbnail['path'] = 'text_content.text'
thumbnail['transform'] = get_thumbnail

# Remove field hi_type
# Add fields title, edition, languages
texts.options['filter_order'] = ['repo_place', 'repo_city', 'edition', 'languages', 'text_type', 'hi_date']
texts.options['column_order'] = ['url', 'title', 'languages', 'text_type', 'hi_date', 'shelfmark',
                                 'repo_place', 'repo_city', 'edition', 'thumbnail']

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

# Remove fields hand_label, hand_date, hand_place, is_described, chartype, character_form
# Add field ontograph
graphs.options['filter_order'] = ['ontograph', 'character', 'allograph', 'repo_place', 'repo_city']
graphs.options['column_order'] = ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date', 'allograph', 'thumbnail']

# FACETED SEARCH: PEOPLE
FACETED_SEARCH['types'].append({
    'disabled': False,
    'key': 'characters',
    'label': 'People',
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

        {'key': 'place', 'label': 'Place', 'path':
         'geographical_origin.name',
         'type': 'title', 'viewable': True, 'search': True, 'count': True},

        {'key': 'texts', 'label': 'Texts',
         'path': 'texts.all.title',
         'type': 'title', 'viewable': True, 'search': True, 'multivalued': True},

        # {'key': 'thumbnail', 'label': 'Thumbnail',
        #  'path': '', 'viewable': True, 'type': 'image'},
    ],
    'filter_order': ['type', 'age', 'gender', 'religion', 'place'],
    'column_order': ['url', 'name', 'variants', 'titles', 'occupations', 'traits', 'type', 'place', 'texts'],
})
