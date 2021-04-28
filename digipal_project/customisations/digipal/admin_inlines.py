import digipal.admin_inlines


####################################################
### BONHUM - Rewriting of class PartLayoutInline ###
###                                              ###
### BEGINNING                                    ###
####################################################

# MODIFICATIONS
# - excluded fields from the inline displayed in item_part:
# tramline_width, on_top_line, multiple_sheet_rulling, bilinear_ruling, hair_arrangement, insular_pricking

class PartLayoutInline(digipal.admin_inlines.PartLayoutInline):
    exclude = ('historical_item', 'tramline_width', 'on_top_line',
                'multiple_sheet_rulling', 'bilinear_ruling', 'hair_arrangement', 'insular_pricking')

####################################################
### END                                          ###
###                                              ###
### BONHUM - Rewriting of class PartLayoutInline ###
####################################################


####################################################
### BONHUM - Rewriting of class ItemLayoutInline ###
###                                              ###
### BEGINNING                                    ###
####################################################

# MODIFICATIONS
# - excluded fields from the inline displayed in historical_item:
# tramline_width, on_top_line, multiple_sheet_rulling, bilinear_ruling, hair_arrangement, insular_pricking

class ItemLayoutInline(digipal.admin_inlines.ItemLayoutInline):
    exclude = ('item_part', 'tramline_width', 'on_top_line',
                'multiple_sheet_rulling', 'bilinear_ruling', 'hair_arrangement', 'insular_pricking')

####################################################
### END                                          ###
###                                              ###
### BONHUM - Rewriting of class ItemLayoutInline ###
####################################################


################################################
### BONHUM - Rewriting of class ScribeInline ###
###                                          ###
### BEGINNING                                ###
################################################

# MODIFICATIONS
# - added a method get_formset to remove the possibility to add or change a contributor type
# while adding/editing a contributor inside an institution

class ScribeInline(digipal.admin_inlines.ScribeInline):

    # FIELD TYPE
    # We don't want the user to be able to add or change a contributor type
    # while adding/editing a contributor inside an institution
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(ScribeInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        field = form.base_fields['type']
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        return formset

################################################
### END                                      ###
###                                          ###
### BONHUM - Rewriting of class ScribeInline ###
################################################
