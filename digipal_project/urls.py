from digipal.urls_project import *
from django.conf.urls import patterns, url

# import * from custom views to make sure the redefinition
# of original methods is taken into account

# digipal views
from digipal_project.customisations.digipal.views.search import *
from digipal_project.customisations.digipal.views.annotation import *
from digipal_project.customisations.digipal.views.content_type.search_scribes import *
from digipal_project.customisations.digipal.views.content_type.search_graphs import *

# digipal_text views
from digipal_project.customisations.digipal_text.views.viewer import *

from digipal.views import search
from digipal_text.views import viewer

urlpatterns = patterns(
    '',
    url(
        r'^digipal/(?P<content_type>characters|sources|places)/(?P<objectid>[^/]+)(/(?P<tabid>[^/]+))?(?:/|$)',
        search.record_view
    ),
    url(
        r'^digipal/(?P<content_type>characters|sources|places)(?:/|$)',
        search.index_view
    ),
    url(
        r'^digipal/(?P<object_type>editions|manuscripts)/(?P<object_id>\d+)/texts/(?P<text_id>\d+)/view/tinymce_generated.css',
        viewer.tinymce_generated_css_view
    ),
    url(
        r'^digipal/(?P<object_type>editions|manuscripts)/(?P<object_id>\d+)/texts/(?P<text_id>\d+)/view/(?P<master_location_type>[^/]+)/(?P<master_location>[^/]+)/?$',
        viewer.text_viewer_view,
    ),
    url(
        r'^digipal/(?P<object_type>editions|manuscripts)/(?P<object_id>\d+)/texts/(?P<text_id>\d+)/view/(?P<master_location_type>[^/]+)/?$',
        viewer.text_viewer_view,
    ),
    url(
        r'^digipal/(?P<object_type>editions|manuscripts)/(?P<object_id>\d+)/texts/(?P<text_id>\d+)/view/?$',
        viewer.text_viewer_view,
    ),
    url(
        r'^digipal/(?P<object_type>editions|manuscripts)/(?P<object_id>\d+)/texts/(?P<text_id>\d+)/(?P<content_type>[^/]+)/(?P<location_type>[^/]+)/(?P<location>[^/]*)/?$',
        viewer.text_api_view,
    ),
    url(
        r'^digipal/(?P<object_type>editions|manuscripts)/(?P<object_id>\d+)/texts/(?P<text_id>\d+)/(?P<content_type>[^/]+)/(?P<location_type>[^/]+)/?$',
        viewer.text_api_view,
    ),
    url(
        r'^digipal/(?P<object_type>editions|manuscripts)/(?P<object_id>\d+)/texts/(?P<text_id>\d+)/(?P<content_type>[^/]+)/?$',
        viewer.text_api_view,
    )
)

urlpatterns += patterns('', ('^', include('digipal.urls')))
