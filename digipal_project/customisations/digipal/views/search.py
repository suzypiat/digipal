##############################################
### BONHUM - Rewriting of get_search_types ###
###                                        ###
### BEGINNING                              ###
##############################################

# MODIFICATIONS
# - added import path for SearchCharacters
# - added SearchCharacters in ret

from digipal.views import search

def get_search_types(request=None):
    from digipal.views.content_type.search_hands import SearchHands
    from digipal.views.content_type.search_manuscripts import SearchManuscripts
    from digipal.views.content_type.search_scribes import SearchScribes
    from digipal.views.content_type.search_graphs import SearchGraphs
    from digipal_project.customisations.digipal.views.content_type.search_characters import SearchCharacters
    search_hands = SearchHands()
    from digipal.utils import is_model_visible
    ret = [search_model for search_model in [SearchManuscripts(), search_hands, SearchScribes(),
    SearchCharacters(),
    SearchGraphs(search_hands)] if is_model_visible(search_model.get_model(), request or True)]

    return ret

search.get_search_types = get_search_types

##############################################
### END                                    ###
###                                        ###
### BONHUM - Rewriting of get_search_types ###
##############################################
