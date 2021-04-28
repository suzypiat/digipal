from django.contrib import admin
from models import *
from digipal.admin_inlines import DigiPalInline, DigiPalInlineDynamic
import digipal.admin_forms
from customisations.digipal.models import Text, Image, CurrentItem, Person, Hand


class Bonhum_StoryCharacterNameVariantInline(DigiPalInline):
    model = Bonhum_StoryCharacterNameVariant


class Bonhum_StoryPlaceNameVariantInline(DigiPalInline):
    model = Bonhum_StoryPlaceNameVariant


class Bonhum_StoryCharacterInline(DigiPalInline):
    model = Bonhum_StoryCharacter
    filter_horizontal = ['occupations', 'traits', 'titles']

    # FIELDS TYPE, GENDER, AGE, RELIGION, TITLES, OCCUPATIONS, TRAITS
    # We don't want the user to be able to add or change these fields
    # while adding/editing a story character inside a story place
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(Bonhum_StoryCharacterInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        fields = [
            form.base_fields['type'],
            form.base_fields['gender'],
            form.base_fields['age'],
            form.base_fields['religion'],
            form.base_fields['titles'],
            form.base_fields['occupations'],
            form.base_fields['traits']
        ]
        for field in fields:
            field.widget.can_add_related = False
            field.widget.can_change_related = False
        return formset


class Bonhum_StoryPlaceTextInline(DigiPalInline):
    model = Text
    verbose_name = 'Story Place-Text Relationship'
    verbose_name_plural = 'Story Place-Text Relationships'
    exclude = ['date_sort', 'date', 'name', 'legacy_id', 'categories', 'languages', 'url']

    # FIELD TYPE
    # We don't want the user to be able to add or change a text type
    # while adding/editing a text inside a story place
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(Bonhum_StoryPlaceTextInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        field = form.base_fields['type']
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        return formset


class Bonhum_StoryCharacterTextInline(DigiPalInline):
    model = Text.story_characters.through
    verbose_name = 'Character-Texts Relationship'
    verbose_name_plural = 'Character-Texts Relationships'


class Bonhum_TextStoryCharacterInline(DigiPalInline):
    model = Bonhum_StoryCharacter.texts.through
    verbose_name = 'Text-Character Relationship'
    verbose_name_plural = 'Text-Character Relationships'


class Bonhum_TextSourceInline(DigiPalInline):
    model = Bonhum_Source.texts.through
    verbose_name = 'Text-Source Relationship'
    verbose_name_plural = 'Text-Source Relationships'


class Bonhum_TextImageInline(DigiPalInline):
    model = Image.texts.through
    verbose_name = 'Text-Image Relationship'
    verbose_name_plural = 'Text-Image Relationships'


class Bonhum_CurrentItemWorkInline(DigiPalInline):
    model = Bonhum_Work.current_items.through
    verbose_name = 'Current Item-Work Relationship'
    verbose_name_plural = 'Current Item-Work Relationships'


class Bonhum_WorkCurrentItemInline(DigiPalInline):
    model = CurrentItem.works.through
    verbose_name = 'Work-Current Item Relationship'
    verbose_name_plural = 'Work-Current Item Relationships'


class Bonhum_WorkEditionInline(DigiPalInline):
    model = Bonhum_Edition
    verbose_name = 'Work-Edition Relationship'
    verbose_name_plural = 'Work-Edition Relationships'


class Bonhum_EditionTextInline(DigiPalInline):
    model = Text
    verbose_name = 'Edition-Text Relationship'
    verbose_name_plural = 'Edition-Text Relationships'
    fields = ['reference', 'title', 'type', 'mythological', 'story_start_date', 'story_place']

    # FIELD TYPE
    # We don't want the user to be able to add or change a text type
    # while adding/editing a text inside an edition
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(Bonhum_EditionTextInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        field = form.base_fields['type']
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        return formset


class Bonhum_ItemPartTextInline(DigiPalInline):
    model = Text
    verbose_name = 'Item Part-Text Relationship'
    verbose_name_plural = 'Item Part-Text Relationships'
    fields = ['reference', 'title', 'type', 'mythological', 'story_start_date', 'story_place']


    # FIELD TYPE
    # We don't want the user to be able to add or change a text type
    # while adding/editing a text inside an item part
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(Bonhum_ItemPartTextInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        field = form.base_fields['type']
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        return formset


class Bonhum_ImageTextInline(DigiPalInline):
    model = Text.images.through
    verbose_name = 'Image-Text Relationship'
    verbose_name_plural = 'Image-Text Relationships'


class Bonhum_SourceTextInline(DigiPalInline):
    model = Text.sources.through
    verbose_name = 'Source-Text Relationship'
    verbose_name_plural = 'Source-Text Relationships'


class Bonhum_SourceAuthorInline(DigiPalInline):
    model = Person.sources.through
    verbose_name = 'Source-Author Relationship'
    verbose_name_plural = 'Source-Author Relationships'


class Bonhum_TextCollaboratorInline(DigiPalInline):
    model = Bonhum_Collaborator.texts.through
    verbose_name = 'Collaborator'
    verbose_name_plural = 'Collaborators'

    # FIELD ACTIVITY
    # We don't want the user to be able to add or change an activity
    # while adding/editing a text/collaborator relationship inside a text
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(Bonhum_TextCollaboratorInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        field = form.base_fields['activity']
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        return formset


class Bonhum_CollaboratorTextInline(DigiPalInline):
    model = Text.collaborators.through
    verbose_name = 'Text'
    verbose_name_plural = 'Texts'

    # FIELD ACTIVITY
    # We don't want the user to be able to add or change an activity
    # while adding/editing a text/collaborator relationship inside a collaborator
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(Bonhum_CollaboratorTextInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        field = form.base_fields['activity']
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        return formset


class Bonhum_CatalogueInline(DigiPalInline):
    model = Bonhum_Catalogue
    verbose_name = 'Catalogue Number'
    verbose_name_plural = 'Catalogue Numbers'


class Bonhum_ScribeHandInline(DigiPalInlineDynamic):
    model = Hand
    extra = 5
    form = digipal.admin_forms.HandForm
    filter_horizontal = ['images']
    fieldsets = (
        ('Item Part', {'fields': ('item_part',)}),
        ('Labels and notes', {'fields': ('label', 'num', 'display_note', 'internal_note', 'comments')}),
        ('Images', {'fields': ('images', 'image_from_desc')}),
        ('Place and Date', {'fields': ('assigned_place', 'assigned_date')}),
        ('Appearance and other properties (only if the contributor is a scribe)', {'fields': ('script', 'appearance', 'relevant',
            'latin_only', 'latin_style', 'scribble_only', 'imitative', 'membra_disjecta')}),
    )


class Bonhum_ItemPartHandInline(DigiPalInlineDynamic):
    model = Hand
    extra = 5
    form = digipal.admin_forms.HandForm
    filter_horizontal = ['images']
    fieldsets = (
        ('Contributor', {'fields': ('scribe',)}),
        ('Labels and notes', {'fields': ('label', 'num', 'display_note', 'internal_note', 'comments')}),
        ('Images', {'fields': ('images', 'image_from_desc')}),
        ('Place and Date', {'fields': ('assigned_place', 'assigned_date')})
    )
