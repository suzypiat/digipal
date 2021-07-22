from digipal.templatetags import html_escape


################################################################
### BONHUM - Rewriting of FacetedModel.get_record_field_html ###
###                                                          ###
### BEGINNING                                                ###
################################################################

# MODIFICATIONS
# - changed the way list items are joined: '<br>' instead of '; '
# - added conditions to handle Bonhum_StoryCharacter and Text thumbnails

from digipal.views.faceted_search.faceted_search import FacetedModel

def get_record_field_html(self, record, field_key):
    if not hasattr(field_key, 'get'):
        for field in self.fields:
            if field['key'] == field_key:
                break

    max_size = field.get('max_size', 50)

    ret = self.get_record_field(record, field, True)
    if isinstance(ret, list):
        ret = '<br>'.join(sorted(ret))

    if field['type'] == 'url':
        ret = '<a href="%s" class="btn btn-default btn-sm" title="" data-toggle="tooltip">View</a>' % ret

    if field['type'] == 'django_image':
        ret = html_escape.get_html_from_django_imagefield(
            ret, max_size=max_size, lazy=1
        )

    if field['type'] == 'image':
        if 'Annotation' in str(type(ret)):
            if 'Graph' or 'Bonhum_StoryCharacter' in str(type(record)):
                if 'Graph' in str(type(record)):
                    ret = html_escape.annotation_img(ret, lazy=1, a_title=record.get_short_label(),
                    a_data_placement="bottom", a_data_toggle="tooltip", a_data_container="body",
                    wrap=record, link=record)
                if 'Bonhum_StoryCharacter' in str(type(record)):
                    ret = html_escape.annotation_img(ret, lazy=1, a_title=record.get_first_graph().get_short_label(),
                    a_data_placement="bottom", a_data_toggle="tooltip", a_data_container="body",
                    wrap=record.get_first_graph(), link=record)
            else:
                ret = html_escape.annotation_img(
                    ret, lazy=1, fixlen=800, wrap=record, link=record
                )
        else:
            if 'Image' in str(type(ret)) and 'TextContentXML' in str(type(record)):
                ret = html_escape.iip_img(
                    ret, width=max_size,
                    lazy=1, wrap=ret, link=record
                )
            else:
                link = ret
                if field.get('link_to_record', False):
                    link = record
                ret = html_escape.iip_img(
                    ret, width=max_size,
                    lazy=1, wrap=link, link=link
                )
    if ret is None:
        ret = ''

    return ret

FacetedModel.get_record_field_html = get_record_field_html

################################################################
### END                                                      ###
###                                                          ###
### BONHUM - Rewriting of FacetedModel.get_record_field_html ###
################################################################
