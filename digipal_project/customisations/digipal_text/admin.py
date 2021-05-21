from django.contrib import admin
from digipal_text.models import TextContent
import digipal_text.admin


####################################################
### BONHUM - Rewriting of class TextContentAdmin ###
###                                              ###
### BEGINNING                                    ###
####################################################

# MODIFICATIONS
# - changed method text_content_form_action_edit_message
# - changed class TextContentForm

from digipal_text.admin import MessageField, ModelFormWithMessageFields

def text_content_form_action_edit_message(text_content):
    ret = u''
    if text_content and text_content.pk and (text_content.item_part or text_content.edition):
        ret = u'<a href="%s">Edit the Text</a>' % text_content.get_absolute_url()
    return ret

class TextContentForm(ModelFormWithMessageFields):
    action_edit = MessageField(
        message=text_content_form_action_edit_message,
        label='Action'
    )

    class Meta:
        fields = '__all__'
        model = TextContent


# MODIFICATIONS
# - changed list_display to add edition
# - changed search_fields to add edition__title
# - changed search_fields to replace text__name by text__title
# - changed fieldsets to remove item_part and type

class TextContentAdmin(digipal_text.admin.TextContentAdmin):
    form = TextContentForm
    list_display = ['text', 'item_part', 'edition', 'type', 'get_string_from_languages', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['item_part__display_label', 'edition__title',
                     'text__title', 'languages__name', 'type__name']
    fieldsets = (
        (None, {'fields': ('text', 'languages')}),
        ('Attribution', {'fields': ('attribution', )}),
        ('Actions', {'fields': ('action_edit', )}),
    )


admin.site.unregister(TextContent)
admin.site.register(TextContent, TextContentAdmin)


####################################################
### END                                          ###
###                                              ###
### BONHUM - Rewriting of class TextContentAdmin ###
####################################################
