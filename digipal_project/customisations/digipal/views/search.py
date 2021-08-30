##############################################
### BONHUM - Rewriting of get_search_types ###
###                                        ###
### BEGINNING                              ###
##############################################

# MODIFICATIONS
# - removed SearchHands
# - added SearchCharacters, SearchSources, SearchPlaces and SearchTexts

from digipal.views import search

def get_search_types(request=None):
    from digipal.views.content_type.search_manuscripts import SearchManuscripts
    from digipal.views.content_type.search_scribes import SearchScribes
    from digipal.views.content_type.search_graphs import SearchGraphs
    from digipal_project.customisations.digipal.views.content_type.search_characters import SearchCharacters
    from digipal_project.customisations.digipal.views.content_type.search_sources import SearchSources
    from digipal_project.customisations.digipal.views.content_type.search_places import SearchPlaces
    from digipal_project.customisations.digipal.views.content_type.search_texts import SearchTexts
    from digipal.utils import is_model_visible
    ret = [search_model for search_model in [SearchManuscripts(), SearchScribes(),
    SearchTexts(), SearchGraphs(), SearchCharacters(), SearchSources(), SearchPlaces()]
    if is_model_visible(search_model.get_model(), request or True)]

    return ret

search.get_search_types = get_search_types

##############################################
### END                                    ###
###                                        ###
### BONHUM - Rewriting of get_search_types ###
##############################################
