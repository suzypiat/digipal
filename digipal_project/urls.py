from digipal.urls_project import *
from django.conf.urls import patterns, url

# import * from custom views to make sure the redefinition
# of original methods is taken into account
from digipal_project.customisations.digipal.views.search import *
from digipal_project.customisations.digipal.views.annotation import *
from digipal_project.customisations.digipal.views.content_type.search_content_type import *
from digipal_project.customisations.digipal.views.content_type.search_scribes import *
from digipal_project.customisations.digipal.views.content_type.search_graphs import *

from digipal.views import search

urlpatterns = patterns(
    '',
    url(
        r'^digipal/(?P<content_type>characters)/(?P<objectid>[^/]+)(/(?P<tabid>[^/]+))?(?:/|$)',
        search.record_view,
    ),
)

urlpatterns += patterns('', ('^', include('digipal.urls')))
