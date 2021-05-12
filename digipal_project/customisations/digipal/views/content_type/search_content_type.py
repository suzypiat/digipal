#########################################################
### BONHUM - Rewriting of SearchContentType.get_model ###
###                                                   ###
### BEGINNING                                         ###
#########################################################

# MODIFICATIONS
# - added a if/else to avoid an error with Iconography,
# since the label has been overwritten

from digipal.views.content_type.search_content_type import SearchContentType

def get_model(self):
    import digipal.models
    if self.label == 'Iconography':
        ret = getattr(digipal.models, 'Graph')
    else:
        ret = getattr(digipal.models, self.label[:-1])
    return ret

SearchContentType.get_model = get_model

#########################################################
### END                                               ###
###                                                   ###
### BONHUM - Rewriting of SearchContentType.get_model ###
#########################################################
