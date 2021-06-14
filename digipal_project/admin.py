from django.contrib import admin
from models import *
import reversion
import admin_inlines
from customisations.digipal.admin import *
from customisations.digipal_text.admin import *

#-----------------------------------------------------------
# TODO: move this to digipal lib
'''
MessageField(message=''|lambda obj)

a new field that can be added to a form.
it will display the message on the form.
The message is either a string or a function of the model instance that returns a string.
'''

#########################
#                       #
#   Story Place         #
#                       #
#########################

class Bonhum_StoryPlaceTypeAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryPlaceType
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class Bonhum_StoryPlaceNatureAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryPlaceNature
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class Bonhum_StoryPlaceAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryPlace
    list_display = ['name', 'type', 'nature', 'parent', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name', 'parent__name', 'parent__parent__name', 'bonhum_storyplacenamevariant__name']
    list_filter = ['type', 'nature']
    inlines = [
        admin_inlines.Bonhum_StoryPlaceNameVariantInline,
        admin_inlines.Bonhum_StoryCharacterInline,
        admin_inlines.Bonhum_StoryPlaceTextInline
    ]

    # FIELDS TYPE AND NATURE
    # We don't want the user to be able to add or change a type or a nature
    # while adding/editing a story place
    def get_form(self, request, obj=None, **kwargs):
        form = super(Bonhum_StoryPlaceAdmin, self).get_form(request, obj, **kwargs)
        fields = [
            form.base_fields['type'],
            form.base_fields['nature']
        ]
        for field in fields:
            field.widget.can_add_related = False
            field.widget.can_change_related = False
        return form


class Bonhum_StoryPlaceNameVariantAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryPlaceNameVariant
    list_display = ['name', 'place', 'language', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name', 'place__name']
    list_filter = ['language']


#########################
#                       #
#   Story Character     #
#                       #
#########################

class Bonhum_StoryCharacterAgeAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryCharacterAge
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class Bonhum_StoryCharacterGenderAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryCharacterGender
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class Bonhum_StoryCharacterTypeAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryCharacterType
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class Bonhum_StoryCharacterReligionAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryCharacterReligion
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class Bonhum_StoryCharacterTitleAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryCharacterTitle
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class Bonhum_StoryCharacterOccupationAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryCharacterOccupation
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class Bonhum_StoryCharacterTraitAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryCharacterTrait
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class Bonhum_StoryCharacterNameVariantAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryCharacterNameVariant
    list_display = ['name', 'character', 'language', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name', 'character__name']
    list_filter = ['language']

class Bonhum_StoryCharacterAdmin(reversion.VersionAdmin):
    model = Bonhum_StoryCharacter
    list_display = ['name', 'type', 'gender', 'age', 'religion', 'geographical_origin', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name', 'bonhum_storycharacternamevariant__name']
    list_filter = ['type', 'gender', 'age', 'religion', 'titles', 'traits', 'occupations']
    fieldsets = (
        (None, {'fields': ('name', 'type', 'gender', 'age', 'religion', 'geographical_origin')}),
        (None, {'fields': ('id_viaf', 'get_viaf_url')}),
        (None, {'fields': ('titles',)}),
        (None, {'fields': ('occupations',)}),
        (None, {'fields': ('traits',)})
    )
    filter_horizontal = ['occupations', 'traits', 'titles']
    readonly_fields = ['get_viaf_url']
    inlines = [
        admin_inlines.Bonhum_StoryCharacterNameVariantInline,
        admin_inlines.Bonhum_StoryCharacterTextInline,
        admin_inlines.Bonhum_StoryCharacterImageInline
    ]

    # FIELDS TYPE, GENDER, AGE, RELIGION, TITLES, OCCUPATIONS, TRAITS
    # We don't want the user to be able to add or change these fields
    # while adding/editing a story character
    def get_form(self, request, obj=None, **kwargs):
        form = super(Bonhum_StoryCharacterAdmin, self).get_form(request, obj, **kwargs)
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
        return form


#########################
#                       #
#   Source              #
#   Work                #
#   Edition             #
#                       #
#########################


class Bonhum_SourceTypeAdmin(reversion.VersionAdmin):
    model = Bonhum_SourceType
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class Bonhum_SourceAdmin(reversion.VersionAdmin):
    model = Bonhum_Source
    list_display = ['title', 'reference', 'type', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['title', 'reference', 'type__name']
    list_filter = ['type']
    fieldsets = (
        (None, { 'fields': ('reference', 'title', 'type') } ),
    )
    inlines = [
        admin_inlines.Bonhum_SourceTextInline,
        admin_inlines.Bonhum_SourceAuthorInline
    ]

    # FIELD TYPE
    # We don't want the user to be able to add or change a type
    # while adding/editing a source
    def get_form(self, request, obj=None, **kwargs):
        form = super(Bonhum_SourceAdmin, self).get_form(request, obj, **kwargs)
        field = form.base_fields['type']
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        return form


class Bonhum_TextTypeAdmin(reversion.VersionAdmin):
    model = Bonhum_TextType
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class Bonhum_WorkAdmin(reversion.VersionAdmin):
    model = Bonhum_Work
    list_display = ['title', 'date', 'language', 'original_version', 'translator', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['title', 'date']
    fieldsets = (
        (None, { 'fields': ('title', 'date') } ),
        (None, { 'fields': ('language', 'original_version', 'translator') } ),
        ('Related Item Parts', { 'fields': ('get_item_parts',) } ),
        ('Related Texts', { 'fields': ('get_texts_by_edition','get_texts_by_item_part') } )
    )
    readonly_fields = ['get_texts_by_edition', 'get_texts_by_item_part', 'get_item_parts']
    inlines = [
        admin_inlines.Bonhum_WorkEditionInline,
        admin_inlines.Bonhum_WorkCurrentItemInline
    ]

    class Media:
        js = ('digipal_project/admin/js/work.js',)


class Bonhum_WorkCurrentItemAdmin(reversion.VersionAdmin):
    model = Bonhum_WorkCurrentItem
    list_display = ['current_item', 'work', 'work_title', 'complete_work', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['current_item__display_label', 'current_item__repository__name', 'current_item__shelfmark', 'work__title', 'work_title']


class Bonhum_EditionAdmin(reversion.VersionAdmin):
    model = Bonhum_Edition
    list_display = ['title', 'date', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['title', 'date', 'editor__name', 'publisher', 'work__title', 'work_title']
    fieldsets = (
        (None, { 'fields': ('title', 'editor', 'publisher', 'date') } ),
        (None, { 'fields': ('work', 'complete_work', 'work_title', 'comments') } )
    )
    inlines = [
        admin_inlines.Bonhum_EditionTextInline
    ]


class Bonhum_ActivityAdmin(reversion.VersionAdmin):
    model = Bonhum_Activity
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class Bonhum_CollaboratorAdmin(reversion.VersionAdmin):
    model = Bonhum_Collaborator
    list_display = ['first_name', 'last_name', 'institution', 'email', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['first_name', 'last_name', 'institution', 'email']
    inlines = [
        admin_inlines.Bonhum_CollaboratorTextInline
    ]


#########################
#                       #
#   Contributor         #
#                       #
#########################


class Bonhum_ContributorTypeAdmin(reversion.VersionAdmin):
    model = Bonhum_ContributorType
    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


#########################
#                       #
#   Catalogue           #
#                       #
#########################


class Bonhum_CatalogueAdmin(reversion.VersionAdmin):
    model = Bonhum_Catalogue
    list_display = ['current_item', 'reference', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['reference', 'current_item__display_label', 'current_item__repository__name', 'current_item__shelfmark']


# Prosopography - Story Place
admin.site.register(Bonhum_StoryPlaceType, Bonhum_StoryPlaceTypeAdmin)
admin.site.register(Bonhum_StoryPlaceNature, Bonhum_StoryPlaceNatureAdmin)
admin.site.register(Bonhum_StoryPlace, Bonhum_StoryPlaceAdmin)
admin.site.register(Bonhum_StoryPlaceNameVariant, Bonhum_StoryPlaceNameVariantAdmin)
# Prosopography - Story Character
admin.site.register(Bonhum_StoryCharacterAge, Bonhum_StoryCharacterAgeAdmin)
admin.site.register(Bonhum_StoryCharacterGender, Bonhum_StoryCharacterGenderAdmin)
admin.site.register(Bonhum_StoryCharacterType, Bonhum_StoryCharacterTypeAdmin)
admin.site.register(Bonhum_StoryCharacterReligion, Bonhum_StoryCharacterReligionAdmin)
admin.site.register(Bonhum_StoryCharacterTitle, Bonhum_StoryCharacterTitleAdmin)
admin.site.register(Bonhum_StoryCharacterOccupation, Bonhum_StoryCharacterOccupationAdmin)
admin.site.register(Bonhum_StoryCharacterTrait, Bonhum_StoryCharacterTraitAdmin)
admin.site.register(Bonhum_StoryCharacter, Bonhum_StoryCharacterAdmin)
admin.site.register(Bonhum_StoryCharacterNameVariant, Bonhum_StoryCharacterNameVariantAdmin)
# Text
admin.site.register(Bonhum_SourceType, Bonhum_SourceTypeAdmin)
admin.site.register(Bonhum_Source, Bonhum_SourceAdmin)
admin.site.register(Bonhum_TextType, Bonhum_TextTypeAdmin)
admin.site.register(Bonhum_Work, Bonhum_WorkAdmin)
admin.site.register(Bonhum_Edition, Bonhum_EditionAdmin)
admin.site.register(Bonhum_WorkCurrentItem, Bonhum_WorkCurrentItemAdmin)
admin.site.register(Bonhum_Activity, Bonhum_ActivityAdmin)
admin.site.register(Bonhum_Collaborator, Bonhum_CollaboratorAdmin)
# Contributor
admin.site.register(Bonhum_ContributorType, Bonhum_ContributorTypeAdmin)
# Catalogue
admin.site.register(Bonhum_Catalogue, Bonhum_CatalogueAdmin)
