from django import forms
import digipal.admin_forms

############################################
### BONHUM - Rewriting of fieldsets_hand ###
###                                      ###
### BEGINNING                            ###
############################################

# MODIFICATIONS
# - renamed block 'Item Part and Scribe' to 'Item Part and Contributor'
# - added contributor_type in block 'Item Part and Contributor'
# - removed block 'Other Catalogues', with fields legacy_id, ker, scragg, em_title
# - removed block 'Gloss', with fields glossed_text, num_glossing_hands, num_glosses, gloss_only
# - renamed block 'Appearance and other properties' to 'Appearance and other properties (only if the contributor is a scribe)'

fieldsets_hand = (
    ('Item Part and Contributor', {'fields': ('item_part', 'contributor_type', 'scribe')}),
    ('Labels and notes', {'fields': ('label', 'num', 'display_note', 'internal_note', 'comments')}),
    ('Images', {'fields': ('images', 'image_from_desc')}),
    ('Place and Date', {'fields': ('assigned_place', 'assigned_date')}),
    ('Appearance and other properties (only if the contributor is a scribe)', {'fields': ('script', 'appearance', 'relevant',
        'latin_only', 'latin_style', 'scribble_only', 'imitative', 'membra_disjecta')}),
)


############################################
### END                                  ###
###                                      ###
### BONHUM - Rewriting of fieldsets_hand ###
############################################



############################################
### BONHUM - Rewriting of class HandForm ###
###                                      ###
### BEGINNING                            ###
############################################

# MODIFICATIONS
# - added field contributor_type

class HandForm(digipal.admin_forms.HandForm):
    contributor_type = forms.CharField(widget=forms.Select, required=False,
                       help_text='A helper to filter the list of contributors according to their type.')

############################################
### END                                  ###
###                                      ###
### BONHUM - Rewriting of class HandForm ###
############################################
