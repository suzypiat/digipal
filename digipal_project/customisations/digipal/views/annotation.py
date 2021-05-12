from digipal.models import Image, Annotation, Hand, Repository, has_edit_permission
from collections import OrderedDict
from django.utils.safestring import mark_safe
from django.core import urlresolvers
from digipal.forms import ImageAnnotationForm
from mezzanine.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

###################################
### BONHUM - Rewriting of image ###
###                             ###
### BEGINNING                   ###
###################################

# MODIFICATIONS
# - added labels for fields Hand (Type) and Alllograph (Motive)

from digipal.views import annotation

def image(request, image_id):
    """The view for the front-end annotator page"""
    from digipal.utils import request_invisible_model, raise_404

    try:
        image = Image.objects.get(id=image_id)
    except Image.DoesNotExist:
        raise_404('This Image record does not exist')

    # 404 if content type Image not visible
    request_invisible_model(Image, request, 'Image')

    # 404 if image is private and user not staff
    if image.is_private_for_user(request):
        raise_404('This Image is currently not publicly available')

    is_admin = has_edit_permission(request, Image)

    # annotations_count = image.annotation_set.all().values('graph').count()
    # annotations = image.annotation_set.all()
    annotations = Annotation.objects.filter(
        image_id=image_id, graph__isnull=False
    ).exclude_hidden(is_admin).select_related(
        'graph__hand', 'graph__idiograph__allograph'
    )
    dimensions = {
        'width': image.dimensions()[0],
        'height': image.dimensions()[1]
    }
    hands = image.hands.count()
    url = request.path
    url = url.split('/')
    url.pop(len(url) - 1)
    url = url[len(url) - 1]
    # Check for a vector_id in image referral, if it exists the request has
    # come via Scribe/allograph route
    vector_id = request.GET.get(
        'graph', '') or request.GET.get('vector_id', '')
    hands_list = []
    hand = {}
    hands_object = Hand.objects.filter(images=image_id)
    data_allographs = OrderedDict()

    for h in hands_object.values():
        if h['label'] == None:
            label = "None"
        else:
            label = mark_safe(h['label'])
        hand = {'id': h['id'], 'name': label.encode('cp1252')}
        hands_list.append(hand)

    # annotations by allograph
    for a in annotations:
        if a.graph and a.graph.hand:
            hand_label = a.graph.hand
            allograph_name = a.graph.idiograph.allograph
            if hand_label in data_allographs:
                if allograph_name not in data_allographs[hand_label]:
                    data_allographs[hand_label][allograph_name] = []
            else:
                data_allographs[hand_label] = OrderedDict()
                data_allographs[hand_label][allograph_name] = []
            data_allographs[hand_label][allograph_name].append(a)

    image_link = urlresolvers.reverse(
        'admin:digipal_image_change', args=(image.id,))
    form = ImageAnnotationForm(auto_id=False)
    form.fields['hand'].queryset = image.hands.all()

    ##############################################
    ### BONHUM - Rewriting of annotation.image ###
    ##############################################
    form.fields['hand'].label = 'Type'
    form.fields['allograph'].label = 'Motive'
    ##############################################
    ### BONHUM - Rewriting of annotation.image ###
    ##############################################

    width, height = image.dimensions()
    image_server_url = image.zoomify
    zoom_levels = settings.ANNOTATOR_ZOOM_LEVELS

    from digipal.models import OntographType
    from digipal.utils import is_model_visible

    images = Image.objects.none()
    if image.item_part:
        images = image.item_part.images.exclude(
            id=image.id).prefetch_related('hands', 'annotation_set')
        images = Image.filter_permissions_from_request(images, request)
        images = Image.sort_query_set_by_locus(images, True)

    from digipal_text.models import TextContentXML

    context = {
        'form': form.as_ul(), 'dimensions': dimensions,
        'images': images,
        'image': image, 'height': height, 'width': width,
        'image_server_url': image_server_url, 'hands_list': hands_list,
        'image_link': image_link, 'annotations': annotations.count(),
        'annotations_list': data_allographs, 'url': url,
        'hands': hands, 'is_admin': is_admin,
        'no_image_reason': image.get_media_unavailability_reason(),
        # True is the user can edit the database
        'can_edit': has_edit_permission(request, Annotation),
        'ontograph_types': OntographType.objects.order_by('name'),
        'zoom_levels': zoom_levels,
        'repositories': Repository.objects.filter(currentitem__itempart__images=image_id),
        # hide all annotations and all annotation tools from the user
        'hide_annotations': int(not is_model_visible('graph', request)),
        'PAGE_IMAGE_SHOW_MSDATE': settings.PAGE_IMAGE_SHOW_MSDATE,
        'text_content_xmls': TextContentXML.objects.filter(text_content__item_part=image.item_part),
    }

    if settings.PAGE_IMAGE_SHOW_MSSUMMARY:
        context['document_summary'] = image.get_document_summary()

    context['annotations_switch_initial'] = 1 - int(context['hide_annotations'] or (
        (request.GET.get('annotations', 'true')).strip().lower() in ['0', 'false']))

    context['show_image'] = context['can_edit'] or not context['no_image_reason']

    if vector_id:
        context['vector_id'] = vector_id

    return render_to_response('digipal/image_annotation.html', context, context_instance=RequestContext(request))


annotation.image = image

###################################
### END                         ###
###                             ###
### BONHUM - Rewriting of image ###
###################################
