from django.contrib import admin
from digipal.models import CharacterForm, Character, \
    CurrentItem, Hand, HistoricalItem, Idiograph, ItemPart, Image, \
    Person, Place, Scribe, Text, Institution
import digipal.admin
import digipal.admin_inlines
import digipal.admin_filters
import digipal_project.admin_inlines
import digipal_project.customisations.digipal.admin_inlines
import digipal_project.customisations.digipal.admin_forms


######################################################
### BONHUM - Rewriting of class CharacterFormAdmin ###
###                                                ###
### BEGINNING                                      ###
######################################################

# MODIFICATIONS
# - changed list_display to add created and modified

class CharacterFormAdmin(digipal.admin.CharacterFormAdmin):
    list_display = ['id', 'name', 'created', 'modified']
    list_display_links = list_display


admin.site.unregister(CharacterForm)
admin.site.register(CharacterForm, CharacterFormAdmin)

######################################################
### END                                            ###
###                                                ###
### BONHUM - Rewriting of class CharacterFormAdmin ###
######################################################


##################################################
### BONHUM - Rewriting of class CharacterAdmin ###
###                                            ###
### BEGINNING                                  ###
##################################################

# MODIFICATIONS
# - changed list_display to add ontograph
# - changed search_fields to add ontograph__name

class CharacterAdmin(digipal.admin.CharacterAdmin):
    list_display = ['name', 'unicode_point', 'ontograph', 'form', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name', 'form__name', 'ontograph__name']


admin.site.unregister(Character)
admin.site.register(Character, CharacterAdmin)

##################################################
### END                                        ###
###                                            ###
### BONHUM - Rewriting of class CharacterAdmin ###
##################################################


####################################################
### BONHUM - Rewriting of class CurrentItemAdmin ###
###                                              ###
### BEGINNING                                    ###
####################################################

# MODIFICATIONS
# - changed fieldsets to add get_item_parts
# - changed readonly_fields to add get_item_parts
# - deleted filter_horizontal to remove owners
# - changed inlines to remove CurrentItemOwnerInline and ItemPartInline
# - changed inlines to add Bonhum_CurrentItemWorkInline and Bonhum_CatalogueInline

class CurrentItemAdmin(digipal.admin.CurrentItemAdmin):
    fieldsets = (
        (None, {'fields': ('display_label', 'repository', 'shelfmark', 'description')}),
        ('Legacy', {'fields': ('legacy_id',)}),
        ('Related Item Parts', { 'fields': ('get_item_parts',)})
    )
    readonly_fields = ['display_label', 'get_item_parts']
    filter_horizontal = []
    inlines = [
        digipal_project.admin_inlines.Bonhum_CurrentItemWorkInline,
        digipal_project.admin_inlines.Bonhum_CatalogueInline
    ]


admin.site.unregister(CurrentItem)
admin.site.register(CurrentItem, CurrentItemAdmin)

####################################################
### END                                          ###
###                                              ###
### BONHUM - Rewriting of class CurrentItemAdmin ###
####################################################


#############################################
### BONHUM - Rewriting of class HandAdmin ###
###                                       ###
### BEGINNING                             ###
#############################################

# MODIFICATIONS
# - changed list_display to remove scragg, script and legacy_id
# - changed list_display_links to remove scragg, script and legacy_id
# - changed search_fields to remove scragg, em_title
# - changed list_filter to remove HandItempPartFilter, HandFilterSurrogates, HandGlossNumFilter, HandGlossTextFilter
# - changed list_filter to add scribe__type
# - removed inlines with HandDescriptionInline, DateEvidenceInline, PlaceEvidenceInline, ProportionInline
# - changed fieldsets (cf. digipal_project.customisations.digipal.admin_forms)
# - changed form (cf. digipal_project.customisations.digipal.admin_forms)
# - added class Media

class HandAdmin(digipal.admin.HandAdmin):
    form = digipal_project.customisations.digipal.admin_forms.HandForm
    fieldsets = digipal_project.customisations.digipal.admin_forms.fieldsets_hand
    list_display = ['id', 'item_part', 'label', 'num', 'scribe',
                    'assigned_date', 'assigned_place', 'created', 'modified']
    list_display_links = ['id', 'item_part', 'label', 'scribe',
                    'assigned_date', 'assigned_place', 'created', 'modified']
    search_fields = ['id', 'legacy_id', 'label', 'num', 'item_part__display_label',
                     'display_note', 'internal_note']
    list_filter = ['latin_only', 'scribe__type', digipal.admin_filters.HandImageNumberFilter]
    inlines = []

    class Media:
        js = ('digipal_project/admin/js/hand.js',)


admin.site.unregister(Hand)
admin.site.register(Hand, HandAdmin)

#############################################
### END                                   ###
###                                       ###
### BONHUM - Rewriting of class HandAdmin ###
#############################################


#######################################################
### BONHUM - Rewriting of class HistoricalItemAdmin ###
###                                                 ###
### BEGINNING                                       ###
#######################################################

# MODIFICATIONS
# - changed fieldsets to remove fields categories, vernacular, neumed, hair, url
# - removed filter_horizontal with categories and owners
# - changed inlines to remove HistoricalItemOwnerInline
# - changed inlines for ItemLayoutInline

class HistoricalItemAdmin(digipal.admin.HistoricalItemAdmin):
    fieldsets = (
        (None, {'fields': ('display_label', 'name', 'date', 'catalogue_number')}),
        ('Classifications', {'fields': ('historical_item_type', 'historical_item_format')}),
        ('Properties', {'fields': ('language',)}),
        ('Legacy', {'fields': ('legacy_id', 'legacy_reference')}),
    )
    filter_horizontal = []
    inlines = [
        digipal.admin_inlines.ItemPartItemInlineFromHistoricalItem,
        digipal.admin_inlines.CatalogueNumberInline,
        digipal.admin_inlines.ItemDateInline,
        digipal.admin_inlines.ItemOriginInline,
        digipal.admin_inlines.CollationInline,
        digipal.admin_inlines.DecorationInline,
        digipal.admin_inlines.DescriptionInline,
        digipal_project.customisations.digipal.admin_inlines.ItemLayoutInline
    ]


admin.site.unregister(HistoricalItem)
admin.site.register(HistoricalItem, HistoricalItemAdmin)

#######################################################
### END                                             ###
###                                                 ###
### BONHUM - Rewriting of class HistoricalItemAdmin ###
#######################################################


#################################################
### BONHUM - Rewriting of class ItemPartAdmin ###
###                                           ###
### BEGINNING                                 ###
#################################################

# MODIFICATIONS
# - changed list_display to remove get_part_count
# - changed list_display to add get_workcurrentitem_currentitem et get_workcurrentitem_work
# - changed search_fields to remove current_item__display_label, subdivisions__display_label, group__display_label
# - changed search_fields to add work_current_item__current_item__display_label et work_current_item__work__title
# - changed list_filter to remove authenticities__category, ItemPartMembersNumberFilter, ItemPartHasGroupGroupFilter
# - changed readonly_fields to add get_workcurrentitem_currentitem, get_workcurrentitem_work
# - changed fieldsets to remove current_item, group, group_locus
# - changed fieldsets to add work_current_item, get_workcurrentitem_currentitem, get_workcurrentitem_work
# - changed inlines to remove ItemSubPartInline, ItemPartAuthenticityInline, ItemPartOwnerInline, TextItemPartInline
# - changed inlines to add Bonhum_ItemPartTextInline
# - changed inlines to replace HandInline by Bonhum_ItemPartHandInline
# - changed inlines for PartLayoutInline
# - removed filter_horizontal with "owners"

class ItemPartAdmin(digipal.admin.ItemPartAdmin):
    list_display = ['id', 'display_label', 'historical_label', 'type',
                    'get_workcurrentitem_currentitem', 'get_workcurrentitem_work',
                    'get_image_count', 'keywords_string',
                    'created', 'modified']
    list_display_links = list_display
    search_fields = ['id', 'locus', 'display_label',
                     'historical_items__display_label',
                     'type__name', 'keywords_string', 'notes',
                     'work_current_item__current_item__display_label',
                     'work_current_item__work__title']
    list_filter = ('type', digipal.admin_filters.ItemPartHIFilter, digipal.admin_filters.ItemPartImageNumberFilter)
    readonly_fields = ('display_label', 'historical_label', 'get_workcurrentitem_currentitem', 'get_workcurrentitem_work')
    filter_horizontal = []
    fieldsets = (
        (None, {'fields': ('display_label','historical_label', 'custom_label', 'type',)}),
        ('This part is currently found in ...', {'fields': ('work_current_item', 'get_workcurrentitem_currentitem', 'get_workcurrentitem_work', 'locus', 'pagination')}),
        ('Notes', {'fields': ('notes', )}),
        ('Keywords', {'fields': ('keywords',)}),
    )
    inlines = [
        digipal.admin_inlines.ItemPartItemInlineFromItemPart,
        digipal_project.admin_inlines.Bonhum_ItemPartHandInline,
        digipal.admin_inlines.ImageInline,
        digipal_project.customisations.digipal.admin_inlines.PartLayoutInline,
        digipal_project.admin_inlines.Bonhum_ItemPartTextInline
    ]


admin.site.unregister(ItemPart)
admin.site.register(ItemPart, ItemPartAdmin)

#################################################
### END                                       ###
###                                           ###
### BONHUM - Rewriting of class ItemPartAdmin ###
#################################################


##############################################
### BONHUM - Rewriting of class ImageAdmin ###
###                                        ###
### BEGINNING                              ###
##############################################

# MODIFICATIONS
# - changed inlines to add Bonhum_ImageTextInline and Bonhum_ImageStoryCharacterInline

class ImageAdmin(digipal.admin.ImageAdmin):
    inlines = [
        digipal.admin_inlines.HandsInline,
        digipal_project.admin_inlines.Bonhum_ImageTextInline,
        digipal_project.admin_inlines.Bonhum_ImageStoryCharacterInline,
    ]


admin.site.unregister(Image)
admin.site.register(Image, ImageAdmin)

##############################################
### END                                    ###
###                                        ###
### BONHUM - Rewriting of class ImageAdmin ###
##############################################


###############################################
### BONHUM - Rewriting of class PersonAdmin ###
###                                         ###
### BEGINNING                               ###
###############################################

# MODIFICATIONS
# - added fieldsets with name, id_viaf and get_viaf_url_with_link
# - excluded legacy_id from fieldsets
# - added readonly_fields with get_viaf_url_with_link
# - removed inlines with OwnerInline

class PersonAdmin(digipal.admin.PersonAdmin):
    inlines = []
    fieldsets = (
        (None, {'fields': ('name',)}),
        (None, {'fields': ('id_viaf', 'get_viaf_url_with_link')})
    )
    readonly_fields = ['get_viaf_url_with_link']


admin.site.unregister(Person)
admin.site.register(Person, PersonAdmin)

###############################################
### END                                     ###
###                                         ###
### BONHUM - Rewriting of class PersonAdmin ###
###############################################


##############################################
### BONHUM - Rewriting of class PlaceAdmin ###
###                                        ###
### BEGINNING                              ###
##############################################

# MODIFICATIONS
# - changed list_display to remove current_county, historical_county
# - changed fieldsets to remove current_county, historical_county, eastings, northings, legacy_id
# - changed inlines to remove PlaceEvidenceInline

class PlaceAdmin(digipal.admin.PlaceAdmin):
    list_display = ['name', 'type', 'region', 'created', 'modified']
    list_display_links = list_display
    fieldsets = (
        (None, { 'fields': ('name', 'type') } ),
        (None, { 'fields': ('region',) } )
    )
    inlines = [
        digipal.admin_inlines.InstitutionInline
    ]


admin.site.unregister(Place)
admin.site.register(Place, PlaceAdmin)

##############################################
### END                                    ###
###                                        ###
### BONHUM - Rewriting of class PlaceAdmin ###
##############################################


###############################################
### BONHUM - Rewriting of class ScribeAdmin ###
###                                         ###
### BEGINNING                               ###
###############################################

# MODIFICATIONS
# - changed list_display to add type
# - changed list_display_links to add type
# - changed search_fields to add type__name, scriptorium__name
# - added list_filter with type
# - changed inlines to replace HandInline by Bonhum_ScribeHandInline
# - added a method get_form to remove the possibility to add or change a contributor type

class ScribeAdmin(digipal.admin.ScribeAdmin):
    list_display = ['type', 'name', 'date', 'scriptorium', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['legacy_id', 'name', 'date', 'type__name', 'scriptorium__name']
    list_filter = ['type']
    inlines = [
        digipal_project.admin_inlines.Bonhum_ScribeHandInline,
        digipal.admin_inlines.IdiographInline
    ]

    # FIELD TYPE
    # We don't want the user to be able to add or change a contributor type
    # while adding/editing a contributor
    def get_form(self, request, obj=None, **kwargs):
        form = super(ScribeAdmin, self).get_form(request, obj, **kwargs)
        field = form.base_fields['type']
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        return form


admin.site.unregister(Scribe)
admin.site.register(Scribe, ScribeAdmin)


###############################################
### END                                     ###
###                                         ###
### BONHUM - Rewriting of class ScribeAdmin ###
###############################################


#############################################
### BONHUM - Rewriting of class TextAdmin ###
###                                       ###
### BEGINNING                             ###
#############################################

# MODIFICATIONS
# - added method text_form_action_edit_message
# - added class TextForm

from digipal_text.admin import MessageField, ModelFormWithMessageFields

def text_form_action_edit_message(text):
    ret = u''
    if text and text.pk:
        from digipal_text.models import TextContent, TextContentXML
        text_content, created = TextContent.objects.get_or_create(text=text)
        text_content_xml, created = TextContentXML.objects.get_or_create(text_content=text_content)
        ret = u'<a href="%s">Edit the Text</a>' % text_content.get_absolute_url()
    return ret

class TextForm(ModelFormWithMessageFields):
    action_edit = MessageField(
        message=text_form_action_edit_message,
        label='Action'
    )

    class Meta:
        fields = '__all__'
        model = Text


# MODIFICATIONS
# - added form
# - changed list_display to remove name, date
# - changed list_display to add title, reference, type, item_part, edition
# - changed list_display_links according to list_display
# - changed search_fields to remove name
# - changed search_fields to add title, reference, type__name, item_part__custom_label, edition__title
# - added list_filter with type
# - changed ordering: replaced name by title
# - added fieldsets with reference, title, type, item_part, get_itempart_work, get_itempart_currentitem,
# edition, get_edition_work, mythological, story_start_date, story_place, action_edit
# - added readonly_fields with get_itempart_work, get_itempart_currentitem, get_edition_work
# - changed inlines to remove TextItemPartInline, CatalogueNumberInline, DescriptionInline
# - changed inlines to add Bonhum_TextImageInline, Bonhum_TextSourceInline, Bonhum_TextStoryCharacterInline, Bonhum_TextCollaboratorInline
# - added a class Media with a js file to handle some constraints
# - added a method get_form to remove the possibility to add or change a text type

class TextAdmin(digipal.admin.TextAdmin):
    form = TextForm
    list_display = ['title', 'reference', 'type', 'item_part', 'edition', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['title', 'reference', 'type__name', 'item_part__custom_label', 'edition__title']
    ordering = ['title']
    list_filter = ['type']
    fieldsets = (
        (None, { 'fields': ('reference', 'title', 'type') } ),
        (None, { 'fields': ('item_part', 'get_itempart_work', 'get_itempart_currentitem', 'edition', 'get_edition_work') } ),
        (None, { 'fields': ('mythological', 'story_start_date', 'story_place') } ),
        ('Actions', { 'fields': ('action_edit',) } )
    )
    readonly_fields = ('get_itempart_work', 'get_itempart_currentitem', 'get_edition_work')
    inlines = [
        digipal_project.admin_inlines.Bonhum_TextImageInline,
        digipal_project.admin_inlines.Bonhum_TextSourceInline,
        digipal_project.admin_inlines.Bonhum_TextStoryCharacterInline,
        digipal_project.admin_inlines.Bonhum_TextCollaboratorInline,
    ]

    # FIELD TYPE
    # We don't want the user to be able to add or change a text type
    # while adding/editing a text
    def get_form(self, request, obj=None, **kwargs):
        form = super(TextAdmin, self).get_form(request, obj, **kwargs)
        field = form.base_fields['type']
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        return form

    class Media:
        js = ('digipal_project/admin/js/text.js',)


admin.site.unregister(Text)
admin.site.register(Text, TextAdmin)


#############################################
### END                                   ###
###                                       ###
### BONHUM - Rewriting of class TextAdmin ###
#############################################


####################################################
### BONHUM - Rewriting of class InstitutionAdmin ###
###                                              ###
### BEGINNING                                    ###
####################################################

# MODIFICATIONS
# - changed inlines to replace digipal.admin_inlines.ScribeInline by digipal_project.customisations.digipal.admin_inlines.ScribeInline

class InstitutionAdmin(digipal.admin.InstitutionAdmin):
    inlines = [
        digipal.admin_inlines.OwnerInline,
        digipal_project.customisations.digipal.admin_inlines.ScribeInline
    ]

admin.site.unregister(Institution)
admin.site.register(Institution, InstitutionAdmin)

####################################################
### END                                          ###
###                                              ###
### BONHUM - Rewriting of class InstitutionAdmin ###
####################################################
