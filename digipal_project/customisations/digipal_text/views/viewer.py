from digipal_text.models import TextContentXMLStatus, TextContent, TextContentXML
import re
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.db import transaction
from digipal import utils
from collections import OrderedDict
from mezzanine.conf import settings
from digipal import utils as dputils
import json
from digipal.utils import sorted_natural

from digipal_text.views.viewer import *


# Custom tinymce_generated_css_view: for each button in TEXT_EDITOR_OPTIONS_CUSTOM,
# add css to each item inside a category
def custom_tinymce_generated_css_view():
    options = settings.TEXT_EDITOR_OPTIONS_CUSTOM
    buttons = []
    for button in options.get('buttons'):
        if options.get('buttons')[button].get('categories') is not None:
            categories = options.get('buttons')[button].get('categories')
            items = [ item for category in categories for item in category['items'] ]
            for item in items:

                color_int = 0
                color_darker = item['color']
                try:
                    color_int = int(item['color'].replace('#', ''), 16)
                except ValueError, e:
                    pass
                if color_int:
                    color_darker = max(0, color_int - 0x808080)
                    color_darker = "#%0.6X" % color_darker

                if item['id'] != 'btnPersonName':
                    selector = 'span[data-dpt-ana="' + item['attributes']['ana'] + '"]'
                else:
                    selector = 'span[data-dpt="persName"]'

                abutton = {
                    'selector': selector,
                    'label': item['label'],
                    'background_color': item['color'],
                    'color': color_darker,
                }
                buttons.append(abutton)
    return buttons


############################################
### BONHUM - Rewriting of viewer methods ###
###                                      ###
### BEGINNING                            ###
############################################

# MODIFICATIONS
# - methods changed:
#    . can_user_see_main_text
#    . text_viewer_view
#    . tinymce_generated_css_view
#    . text_api_view
#    . get_tei_from_text_response
#    . get_or_create_text_content_records
#    . text_api_view_location
#    . text_api_view_text
#    . text_api_view_image
#    . get_text_elements_from_image
#    . get_elementid_from_xml_element
# - added condition on the origin of the text to annotate: item_part or edition
# - changed methods parameters and added new ones:
#    . object_type is "manuscripts" or "editions"
#    . object_id is the id of the item_part (ItemPart) or the id of the edition (Bonhum_Edition)
#    . object is the item_part (ItemPart) or the edition (Bonhum_Edition)
#    . text_id is the id of the text (Text) to annotate
#    . text is the text (Text) to annotate

from digipal_text.views import viewer


# Changed parameters: object_type, object, text_id, request
# instead of: itempart, request
# Changed the TextContentXML filter, according to the object_type ("manuscripts" or "editions")
def can_user_see_main_text(object_type, object, text_id, request):
    '''Returns True if the user is staff or the main text for this IP is public'''
    ret = False

    if request.user and request.user.is_active and request.user.is_staff:
        return True

    if object_type == 'manuscripts':
        tcx = TextContentXML.objects.filter(
            text_content__text__item_part=object,
            text_content__text__id=text_id,
            text_content__type__slug='transcription'
        ).first()
    elif object_type == 'editions':
        tcx = TextContentXML.objects.filter(
            text_content__text__edition=object,
            text_content__text__id=text_id,
            text_content__type__slug='edited',
        ).first()

    ret = tcx and not tcx.is_private() and len(tcx.content) > 1

    return ret

viewer.can_user_see_main_text = can_user_see_main_text


# Changed parameters: request, object_type, object_id=0, text_id=0, master_location_type='', master_location=''
# instead of: request, item_partid=0, master_location_type='', master_location=''
# Changed the content of context, according to the object_type ("manuscripts" or "editions")
# Changed parameters for can_user_see_main_text() call
def text_viewer_view(request, object_type, object_id=0, text_id=0,
                     master_location_type='', master_location=''):

    from digipal.utils import is_model_visible
    if not is_model_visible('textcontentxml', request):
        raise Http404('The Text Viewer is not enabled on this site')

    if object_type == 'manuscripts':
        from digipal.models import ItemPart
        context = {'item_partid': object_id,
                   'textid': text_id,
                   'item_part': ItemPart.objects.filter(id=object_id).first()}
        if not context['item_part']:
            raise Http404('This document doesn\'t exist')
        if not can_user_see_main_text('manuscripts', context['item_part'], text_id, request):
            raise Http404('This document is not publicly accessible')
    elif object_type == 'editions':
        from digipal_project.models import Bonhum_Edition
        context = {'editionid': object_id,
                   'textid': text_id,
                   'edition': Bonhum_Edition.objects.filter(id=object_id).first()}
        if not context['edition']:
            raise Http404('This document doesn\'t exist')
        if not can_user_see_main_text('editions', context['edition'], text_id, request):
            raise Http404('This document is not publicly accessible')

    # Define the content of content type and location type drop downs
    # on top of each panel
    if object_type == 'manuscripts':
        context['dd_content_types'] = [
            {'key': 'transcription', 'label': 'Transcription',
                'icon': 'align-left', 'attrs': [['data-class', 'Text']]},
            {'key': 'image', 'label': 'Image', 'icon': 'picture',
                'attrs': [['data-class', 'Image']]},
        ]
    elif object_type == 'editions':
        context['dd_content_types'] = [
            {'key': 'edited', 'label': 'Text edited',
                'icon': 'indent-left', 'attrs': [['data-class', 'Text']]},
        ]

    context['dd_location_types'] = [
        {'key': 'whole', 'label': 'Whole text', 'icon': 'book'},
        {'key': 'locus', 'label': 'Locus', 'icon': 'file'},
        {'key': 'entry', 'label': 'Entry', 'icon': 'entry'},
        {'key': 'section', 'label': 'Section', 'icon': 'section'},
        {'key': 'sync', 'label': 'Synchronise with', 'icon': 'link'},
    ]
    context['dd_download_formats'] = [
        {'key': 'html', 'label': 'HTML', 'icon': 'download'},
        {'key': 'tei', 'label': 'TEI', 'icon': 'download'},
        {'key': 'plain', 'label': 'Plain Text', 'icon': 'download'},
    ]
    context['statuses'] = TextContentXMLStatus.objects.all(
    ).order_by('sort_order')

    context['body_class'] = 'page-text-viewer'

    context['text_editor_options'] = settings.TEXT_EDITOR_OPTIONS

    update_viewer_context(context, request)

    return render(request, 'digipal_text/text_viewer.html', context)

viewer.text_viewer_view = text_viewer_view


# Changed parameters: request, object_type, object_id=0, text_id=0
# instead of: request, item_partid=0
# Added a call to custom_tinymce_generated_css_view() to add the custom buttons
# to the context
def tinymce_generated_css_view(request, object_type, object_id=0, text_id=0):
    '''This view generate a css file based on
        settings.py:TEXT_EDITOR_OPTIONS_CUSTOM['buttons']

        'btnPersonName': {'label': 'Person Name', 'tei': '<rs type="person" subtype="name">{}</rs>'},

        =>

        span[data-tei='rs'][data-tei-type='person'][data-tei-subtype='name'] {

        }
    '''

    rules = '''
    span[data-dpt='rs'][data-dpt-type='person'][data-dpt-subtype='name'] {
        background-color: lightgreen;
    }
    span[data-dpt='rs'][data-dpt-type='person'][data-dpt-subtype='name']:before {
        content: "Person Name";
    }
    .preview.mce-content-body span[data-dpt]:before {
        display: inline-block;
    }
    '''
    options = settings.TEXT_EDITOR_OPTIONS

    buttons = []
    for button in options.get('buttons', {}).values():
        # see panelset.tinymce.js addButtonsFromSettings()
        if not isinstance(button, dict):
            continue
        xml = button.get('xml', None)
        tei = button.get('tei', None)
        tag = button.get('tag', 'span')
        color = button.get('color', '#b0ffb0')
        label = button.get('label', '???')
        is_plain = button.get('plain', 0)

        if tei:
            xml = tei
            xml = re.sub(ur'(\w+)\s*=', ur'data-dpt-\1=', xml)
            xml = re.sub(ur'<\/(\w+)', ur'</' + tag, xml)
            xml = re.sub(ur'<(\w+)', ur'<' + tag + ur' data-dpt="\1"', xml)
        if not xml:
            continue

        # print(xml)
        selector = re.sub(
            ur'''([\w-]+)\s*=\s*(["'][^"']+["'])''', ur'[\1=\2]', xml)
        selector = re.sub(ur'[\s<]', ur'', selector)
        selector = re.sub(ur'>.*', ur'', selector)

        color_int = 0
        color_darker = color
        try:
            color_int = int(color.replace('#', ''), 16)
        except ValueError, e:
            pass
        if color_int:
            color_darker = max(0, color_int - 0x808080)
            color_darker = "#%0.6X" % color_darker

        if is_plain:
            color = 'transparent'
            color_darker = 'transparent'
            label = ''

        # selector = '''[data-dpt='rs'][data-dpt-type='person'][data-dpt-subtype='name']'''
        abutton = {
            'selector': selector,
            'label': label,
            'background_color': color,
            'color': color_darker,
        }
        buttons.append(abutton)

    custom_buttons = custom_tinymce_generated_css_view()
    buttons = buttons + custom_buttons

    context = {
        'buttons': buttons,
        'show_highlights_in_preview': options.get('show_highlights_in_preview', 0),
    }
    return render(request, 'digipal_text/tinymce_generated_css.html', context, content_type='text/css')

viewer.tinymce_generated_css_view = tinymce_generated_css_view


# Changed parameters: request, object_type, object_id, text_id, content_type, location_type=u'default', location=''
# instead of: request, item_partid, content_type, location_type=u'default', location=''
# Changed parameters for text_api_view_content_type() call
def text_api_view(request, object_type, object_id, text_id, content_type,
                  location_type=u'default', location=''):

    format = dputils.get_request_var(request, 'format', 'html').strip().lower()
    if request.is_ajax():
        format = 'json'

    from digipal.utils import is_model_visible
    if not is_model_visible('textcontentxml', request):
        raise Http404('Text view not enabled')
    max_size = MAX_FRAGMENT_SIZE if format == 'json' else None

    response = None

    # DELEGATE TO A CUSTOM VIEW FOR THE GIVEN CONTENT TYPE

    # Look up the content_type in the function name
    # e.g. content_type = image => text_api_view_image
    text_api_view_content_type = globals().get(
        'text_api_view_' + content_type, None)
    content_type_record = None

    if not text_api_view_content_type:
        # Look up the content_type in the TextContentType table
        # e.g. content_type = translation or transcription, we assume it must
        # be a TextContentXML
        from digipal_text.models import TextContentType
        content_type_record = TextContentType.objects.filter(
            slug=content_type).first()

        if content_type_record:
            text_api_view_content_type = text_api_view_text

    if text_api_view_content_type:
        response = text_api_view_content_type(
            request, object_type, object_id, text_id, content_type,
            location_type, location, content_type_record, max_size=max_size)

    # we didn't find a custom function for this content type
    if response is None:
        response = {'status': 'error',
                    'message': 'Invalid Content Type (%s)' % content_type}

    # If sublocation is not defined by specific function we just return
    # the desired sublocation.
    # If specific function want to remove they can set it to []
    response['sub_location'] = response.get(
        'sub_location', get_sub_location_from_request(request))
    if not response['sub_location']:
        del response['sub_location']

    # HANDLE location_type = sync

    # We take care of syncing logic here, customisations don't need to worry
    # about it.
    # Sync in => sync out. For UI/client logic purpose.
    # If we don't return sync, client assumes we can't support sync.
    # Only exception is in resolve_default_location() below.
    if response.get('location_type', '') == 'sync':
        response['location_type'] = location_type
        response['location'] = location
        response['content'] = 'Synchronising panel...'
        set_message(response, 'Synchronising panel...', '')

    ret = None

    # RESPONSE FORMATTING
    if format == 'json':
        ret = HttpResponse(json.dumps(response),
                           content_type='application/json')

    if format == 'html':
        context = {'response': response}
        context['display_classes'] = ' '.join(
            (dputils.get_request_var(request, 'ds', '').split(',')))
        context['content_type_key'] = content_type
        ret = render(request, 'digipal_text/text_view.html', context)

    if format == 'tei':
        tei = get_tei_from_text_response(response, object_type, object_id, text_id, content_type)
        ret = HttpResponse(tei, content_type='text/xml; charset=utf-8')

    if format == 'plain':
        plain_text = dputils.get_plain_text_from_xmltext(
            response.get('attribution', ''), keep_links=True
        ) + '\n\n'
        plain_text += dputils.get_plain_text_from_xmltext(
            response.get('content', '')
        )
        ret = HttpResponse(
            plain_text,
            content_type='text/plain; charset=utf-8'
        )

    if not ret:
        raise Exception('Unknown output format: "%s"' % format)

    return ret

viewer.text_api_view = text_api_view


# Changed parameters: response, object_type, object_id, text_id, content_type
# instead of: response, item_partid, content_type
# Changed the TextContentXML filter, according to the object_type ("manuscripts" or "editions")
# Changed the content of context, according to the object_type ("manuscripts" or "editions")
def get_tei_from_text_response(response, object_type, object_id, text_id, content_type):
    ret = response.get('content', '')

    # decode entities (e.g. &rsquo;)
    # TODO: make sure we keep core XML entities otherwise it may cause
    # parsing errors down the line
    from HTMLParser import HTMLParser
    parser = HTMLParser()
    ret = parser.unescape(ret)
    # convert & back to &amp; to keep XML well-formed
    ret = ret.replace(u'&', u'&amp;')

    # convert to XML object
    #xml = dputils.get_xml_from_unicode(ret, ishtml=True, add_root=True)
    if object_type == 'manuscripts':
        from digipal.models import ItemPart
        itempart = ItemPart.objects.filter(id=object_id).first()
        tcx = TextContentXML.objects.filter(
            text_content__type__slug='transcription', text_content__text__item_part__id=object_id, text_content__text__id=text_id).first()
    elif object_type == 'editions':
        from digipal_project.models import Bonhum_Edition
        edition = Bonhum_Edition.objects.filter(id=object_id).first()
        tcx = TextContentXML.objects.filter(
            text_content__type__slug='edited', text_content__text__edition__id=object_id, text_content__text__id=text_id).first()

    #
    from django.template.loader import render_to_string
    if object_type == 'manuscripts':
        context = {
            'meta': {
                'title': '%s of %s' % (content_type.title(), itempart),
                'ms': {
                    'place': itempart.current_item.repository.place.name,
                    'repository': itempart.current_item.repository.name,
                    'shelfmark': itempart.current_item.shelfmark,
                },
                'edition': {
                    'date': tcx.modified
                },
                'project': settings.SITE_TITLE,
                'authority': settings.SITE_TITLE,
            },
        }
    elif object_type == 'editions':
        context = {
            'meta': {
                'title': '%s of %s' % (content_type.title(), edition),
                'ms': {
                    'place': edition.editor.name,
                },
                'edition': {
                    'date': tcx.modified
                },
                'project': settings.SITE_TITLE,
                'authority': settings.SITE_TITLE,
            },
        }
    template = render_to_string('digipal_text/tei_from_xhtml.xslt', context)
    ret = dputils.get_xslt_transform('<root>%s</root>' % ret, template)

    ret = dputils.get_unicode_from_xml(xmltree=ret).replace('xmlns=""', '')

    # convert XML to string
    #ret = dputils.get_unicode_from_xml(xml, remove_root=True)

    return ret

viewer.get_tei_from_text_response = get_tei_from_text_response


# Changed parameters: object_type, object, text, content_type_record
# instead of: item_part, content_type_record
# Changed call to TextContent.get_or_create(), according to the object_type ("manuscripts" or "editions")
def get_or_create_text_content_records(object_type, object, text, content_type_record):
    '''Returns a TextContentXML record for the given IP and Text Content Type
        Create the records (TextContent, TextContentXML) if needed
        Implements optimistic transaction with multiple attempts
        TODO: review is this is still needed. SInce I have set unique_together
        on the TC and TCX tables, the race condition doesn't appear!
    '''
    ret = None
    created = False
    error = {}
    attempts = 3
    # from django.core.exceptions import MultipleObjectsReturned
    from django.db import IntegrityError
    from threading import current_thread
    for i in range(0, attempts):
        with transaction.atomic():
            # get or create the TextContent
            if object_type == 'manuscripts':
                text_content, created = TextContent.objects.get_or_create(
                    item_part=object, type=content_type_record, text=text)
            elif object_type == 'editions':
                text_content, created = TextContent.objects.get_or_create(
                    edition=object, type=content_type_record, text=text)
            # get or create the TextContentXML
            ret, created = TextContentXML.objects.get_or_create(
                text_content=text_content)
        try:
            with transaction.atomic():
                # get or create the TextContent
                if object_type == 'manuscripts':
                    text_content, created = TextContent.objects.get_or_create(
                        item_part=object, type=content_type_record, text=text)
                elif object_type == 'editions':
                    text_content, created = TextContent.objects.get_or_create(
                        edition=object, type=content_type_record, text=text)
                # get or create the TextContentXML
                ret, created = TextContentXML.objects.get_or_create(
                    text_content=text_content)
        except IntegrityError as e:
            # race condition
            from time import sleep, time
            import random
            # print time(), current_thread().getName(), i, '%s' % e
            sleep(random.random())
            continue
        except Exception as e:
            raise e
            set_message(error, '%s, server error (%s)' %
                        (content_type_record.slug.capitalize(), e))
        break

    if not error and not ret:
        set_message(error, '%s, server error (race conditions)' %
                    (content_type_record.slug.capitalize(),))

    return ret, created, error

viewer.get_or_create_text_content_records = get_or_create_text_content_records


# Changed parameters: request, object_type, object_id, text_id, content_type, location_type, location, user=None, max_size=MAX_FRAGMENT_SIZE
# instead of: request, item_partid, content_type, location_type, location, user=None, max_size=MAX_FRAGMENT_SIZE
# Added condition: resolve_master_location() is called when object_type=="manuscripts", not "editions"
def text_api_view_location(request, object_type, object_id, text_id, content_type,
                           location_type, location, user=None, max_size=MAX_FRAGMENT_SIZE):
    '''This content type is for the list of all available locations (text, images)
        Used by the master location widget on top of the Text Viewer web page
    '''
    from digipal.models import ItemPart, Text

    load_locations = utils.get_int_from_request_var(request, 'load_locations')

    if load_locations and object_type == 'manuscripts':
        context = {'item_part': ItemPart.objects.filter(id=object_id).first()}
        resolve_master_location(context, location_type, location)

        ret = {
            'location_type': context['master_location_type'],
            'location': context['master_location'],
            'locations': context['master_locations'],
            'toc': context.get('master_toc', {'39a2': 'toc2', '39r': 'toc3', '39a1': 'toc1'}),
        }
    else:
        ret = {
            'location_type': location_type,
            'location': location,
        }

    return ret

viewer.text_api_view_location = text_api_view_location


# Changed parameters: request, object_type, object_id, text_id, content_type, location_type, location, content_type_record, user=None, max_size=MAX_FRAGMENT_SIZE
# instead of: request, item_partid, content_type, location_type, location, content_type_record, user=None, max_size=MAX_FRAGMENT_SIZE
# Changed the call to get_or_create_text_content_records() according to the object_type ("manuscripts" or "editions")

# TODO: content_type_record makes this signature non-polymorphic and even incompatible with image
# need to use optional parameter for it
def text_api_view_text(request, object_type, object_id, text_id, content_type, location_type,
                       location, content_type_record, user=None, max_size=MAX_FRAGMENT_SIZE):
    ret = {}

    text_content_xml = None

    if not user and request:
        user = request.user

    # print 'content type %s' % content_type_record
    # 1. Fetch or Create the necessary DB records to hold this text
    from digipal.models import ItemPart, Text
    from digipal_project.models import Bonhum_Edition
    if object_type == 'manuscripts':
        item_part = ItemPart.objects.filter(id=object_id).first()
        text = Text.objects.filter(id=text_id).first()
        if item_part and text:
            # print 'item_part %s' % item_part
            text_content_xml, created, error = get_or_create_text_content_records(
                'manuscripts', item_part, text, content_type_record)
            if error:
                return error
    elif object_type == 'editions':
        edition = Bonhum_Edition.objects.filter(id=object_id).first()
        text = Text.objects.filter(id=text_id).first()
        if edition and text:
            # print 'edition %s' % edition
            text_content_xml, created, error = get_or_create_text_content_records(
                'editions', edition, text, content_type_record)
            if error:
                return error

    if not text_content_xml:
        return set_message(ret, '%s not found' % content_type.capitalize())

    from digipal.utils import is_user_staff
    if not is_user_staff(user):
        if text_content_xml.is_private():
            if text_content_xml.content and len(text_content_xml.content) > 10:
                return set_message(
                    ret, 'The %s will be made available at a later stage of the project' % content_type)
            else:
                return set_message(ret, '%s not found' %
                                   content_type.capitalize())

    record_content = text_content_xml.content or ''

    # 2. Load the list of possible location types and locations
    # return the locus of the entries
    if location_type == 'default' or utils.get_int_from_request_var(
            request, 'load_locations'):
        # whole
        ret['locations'] = OrderedDict()

        # whole
        if max_size is not None and len(record_content) <= max_size and (
                content_type != 'codicology'):
            ret['locations']['whole'] = []

        # entry
        for ltype in ['entry', 'locus']:
            ret['locations'][ltype] = []
            if text_content_xml.content:
                for entry in re.findall(
                        ur'(?:<span data-dpt="location" data-dpt-loctype="' + ltype + '">)([^<]+)', text_content_xml.content):
                    ret['locations'][ltype].append(entry)
            if not ret['locations'][ltype]:
                del ret['locations'][ltype]

    # resolve 'default' location request
    location_type, location = resolve_default_location(
        location_type, location, ret)

    # 3. Save the user fragment
    new_fragment = None
    if request:
        new_fragment = dputils.get_request_var(request, 'content', None)

    convert = utils.get_int_from_request_var(request, 'convert')
    save_copy = utils.get_int_from_request_var(request, 'save_copy')

    ret['content_status'] = text_content_xml.status.id

    extent = get_fragment_extent(record_content, location_type, location)
    ret['message'] = ''
    dry_run = 0
    if extent:
        # make sure we compare with None, as '' is a different case
        if new_fragment is not None:
            ret['message'] = 'Content saved'

            # insert user fragment
            len_previous_record_content = len(record_content)
            # TODO: UNCOMMENT!!!!!!!!!!!!!!!!!!!!!!!!!!
            if not dry_run:
                record_content = record_content[0:extent[0]] + \
                    new_fragment + record_content[extent[1]:]

            # we make a copy if the new content removes 10% of the content
            # this might be due to a bug in the UI
            if len(record_content) < (0.9 * len_previous_record_content):
                print 'Auto copy (smaller content)'
                text_content_xml.save_copy()

            # set the new content
            text_content_xml.content = record_content

            # auto-markup
            if convert:
                text_content_xml.convert()
                record_content = text_content_xml.content
                ret['message'] = 'Content converted and saved'

            # make a copy if user asked for it
            if save_copy:
                text_content_xml.save_copy()
                ret['message'] = 'Content backed up'

            # save the new content
            if not dry_run:
                text_content_xml.save()

            # update the extent
            # note that extent can fail now if the user has remove the marker
            # for the current location
            extent = get_fragment_extent(
                record_content, location_type, location)
        else:
            # auto-markup (without saving, used for testing on the full text
            # view page)
            if convert:
                text_content_xml.convert()
                record_content = text_content_xml.content
                ret['message'] = 'Content converted and saved'

                if utils.get_int_from_request_var(request, '_save'):
                    text_content_xml.save()

                # update the extent
                extent = get_fragment_extent(
                    record_content, location_type, location)

    # 4. now the loading part (we do it in any case, even if saved first)
    if not extent:
        if ret['message']:
            ret['message'] += ' then '
        ret['message'] += 'location not found: %s %s' % (
            location_type, location)
        ret['status'] = 'error'
    else:
        if max_size is not None and (extent[1] - extent[0]) > max_size:
            if ret['message']:
                ret['message'] += ' then '
            ret['message'] += 'text too long (> %s bytes)' % (max_size)
            ret['status'] = 'error'
        else:
            ret['content'] = record_content[extent[0]:extent[1]]
            if new_fragment is None:
                ret['message'] = 'Content loaded'
                if created:
                    ret['message'] += ' (new empty text)'

    # we return the location of the returned fragment
    # this may not be the same as the requested location
    # e.g. if the requested location is 'default' we resolve it
    ret['location_type'] = location_type
    ret['location'] = location

    if text_content_xml:
        attribution = text_content_xml.text_content.attribution
        if attribution and attribution.message:
            message = attribution.message
            message = re.sub('<p>&nbsp;</p>', '', message)
            ret['attribution'] = message
        if attribution:
            message = attribution.get_short_message()
            if message:
                ret['attribution_short'] = message

    return ret

viewer.text_api_view_text = text_api_view_text


# Changed parameters: request, object_type, object_id, text_id, content_type, location_type,
#                     location, content_type_record, max_size=None, ignore_sublocation=False
# instead of: request, item_partid, content_type, location_type, location,
#             content_type_record, max_size=None, ignore_sublocation=False
def text_api_view_image(request, object_type, object_id, text_id, content_type, location_type,
                        location, content_type_record, max_size=None, ignore_sublocation=False):
    '''
        location = an identifier for the image. Relative to the item part
                    '#1000' => image with id = 1000
                    '1r'    => image with locus = 1r attached to selected item part
    '''
    ret = {}

    from digipal.models import Image

    # ##
    # The sub_location can override or contradict (location_type, location)
    # e.g. text: whole -> image: synced with text
    #      user clicks on entry in the text => we need to fetch that part
    if not ignore_sublocation:
        sub_location = get_sub_location_from_request(request)
        new_address = get_address_from_sub_location(sub_location)
        if new_address:
            location_type, location = new_address
    # ##

    request.visible_images = None

    visible_images = None

    def get_visible_images(item_partid, request, visible_images=None):
        if visible_images is None:
            ret = Image.objects.filter(item_part_id=item_partid)
            ret = Image.filter_permissions_from_request(ret, request, True)
            ret = Image.sort_query_set_by_locus(ret)
            visible_images = ret
        return visible_images

    # return the locus of the images under this item part
    # return #ID for images which have no locus
    if location_type == 'default' or utils.get_int_from_request_var(
            request, 'load_locations'):
        recs = Image.sort_query_set_by_locus(get_visible_images(
            object_id, request, visible_images)).values_list('locus', 'id')
        ret['locations'] = OrderedDict()
        if recs:
            ret['locations']['locus'] = ['%s' %
                                         (rec[0] or '#%s' % rec[1]) for rec in recs]

    # resolve 'default' location request
    location_type, location = resolve_default_location(
        location_type, location, ret)

    # find the image
    image = find_image(request, object_id, location_type,
                       location, get_visible_images, visible_images)

    if not image:
        set_message(ret, 'Image not found')
        ret['location_type'] = location_type
        ret['location'] = location
    else:
        if location_type == 'entry':
            # user asked for entry, we can only return a locus
            # so we add the entry as a sublocation
            ret['sub_location'] = ['', 'location'], [
                'loctype', 'entry'], ['@text', location]

        if request.method == 'POST':
            # deal with writing annotations
            update_text_image_link(request, image, ret)
        else:
            # display settings
            ret['presentation_options'] = [
                ["highlight", "Highlight Text Units"]]

            # image dimensions
            options = {}
            layout = dputils.get_request_var(request, 'layout', '')
            if layout == 'width':
                options['width'] = dputils.get_request_var(
                    request, 'width', '100')

            # we return the location of the returned fragment
            # this may not be the same as the requested location
            # e.g. if the requested location is 'default' we resolve it
            # ret['location_type'] = location_type
            ret['location_type'] = 'locus'
            ret['location'] = image.locus if image else location

            if image:
                # ret['content'] = iip_img(image, **options)
                ret['zoomify_url'] = image.zoomify()
                ret['width'] = image.width
                ret['height'] = image.height

                # add all the elements found on that page in the transcription
                # ret['text_elements'] = get_text_elements_from_image(request, item_partid, getattr(settings, 'TEXT_IMAGE_MASTER_CONTENT_TYPE', 'transcription'), location_type, location)
                ret['text_elements'] = get_text_elements_from_image(request, object_type, object_id, text_id, getattr(
                    settings, 'TEXT_IMAGE_MASTER_CONTENT_TYPE', 'transcription'), 'locus', get_locus_from_location(location_type, location))

                # print ret['text_elements']

                # add all the non-graph annotations
                ret.update(get_annotations_from_image(image))

    return ret

viewer.text_api_view_image = text_api_view_image


# Changed parameters: request, object_type, object_id, text_id, content_type, location_type, location
# instead of: request, item_partid, content_type, location_type, location
# Changed the parameters for text_api_view_text() call
def get_text_elements_from_image(
        request, object_type, object_id, text_id, content_type, location_type, location):
    # returns the TRANSCRIPTION text for the requested location
    # if not found, returns the whole text
    # eg.:  "text_elements": [[["", "clause"], ["type", "address"]], [["",
    # "clause"], ["type", "disposition"]], [["", "clause"], ["type",
    # "witnesses"]]]

    ret = []

    from digipal_text.models import TextContentType
    content_type_record = TextContentType.objects.filter(
        slug=content_type).first()

    # find the transcription for that image
    text_info = text_api_view_text(request, object_type, object_id, text_id, content_type, location_type,
                                   location, content_type_record, user=None, max_size=MAX_FRAGMENT_SIZE)
    if text_info.get(
            'status', None) == 'error' and 'location not found' in text_info['message'].lower():
        # location not found, try the whole text
        text_info = text_api_view_text(request, object_type, object_id, text_id, content_type, 'whole',
                                       '', content_type_record, user=None, max_size=MAX_FRAGMENT_SIZE)

    # extract all the elements
    if text_info.get('status', '').lower() != 'error':
        #         print '-' * 80
        #         print location_type, location
        # print text_info.get('location_type'), text_info.get('location')
        content = text_info.get('content', '')
        ret = get_text_elements_from_content(content)

    return ret

viewer.get_text_elements_from_image = get_text_elements_from_image


# Removed the white list to filter the elements:
# it was "clause", "location", "person", but we have more elements
# in text_editor_options_custom now
def get_elementid_from_xml_element(element, idcount, as_string=False):
    ''' returns the elementid as a list
        e.g. [(u'', u'clause'), (u'type', u'disposition')]

        element: an xml element (etree)
        idcount: a dictionary, new for each enclosing text unit. Used to know
            which occurrence of an element we are seeing and generate a
            unique id. E.g. two same titles ('sheriff') marked up in the same
            way within the same entry => we need a count to differentiate
            them. We add [@o, 2] to second occurrence, etc.
    '''
    from django.utils.text import slugify

    element_text = utils.get_xml_element_text(element)

    # eg. parts: [(u'', u'clause'), (u'type', u'disposition')]
    parts = [(unicode(re.sub('data-dpt-?', '', k)), unicode(v))
             for k, v in element.attrib.iteritems() if k.startswith('data-dpt') and k not in ['data-dpt-cat']]

    element_text = slugify(u'%s' % element_text.lower())
    if len(element_text) > 0 and len(element_text) < 20:
        parts.append(['@text', element_text])

    if parts:
        order = dputils.inc_counter(idcount, repr(parts))
        if order > 1:
            # add (u'@o', u'2') if it is the 2nd occurence of this elementid
            parts.append((u'@o', u'%s' % order))

    return parts

viewer.get_elementid_from_xml_element = get_elementid_from_xml_element


############################################
### END                                  ###
###                                      ###
### BONHUM - Rewriting of viewer methods ###
############################################
