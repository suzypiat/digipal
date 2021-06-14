from digipal.models import Allograph, Image, Annotation, Hand, Repository, \
    has_edit_permission
from collections import OrderedDict
from django.utils.safestring import mark_safe
from django.core import urlresolvers
from digipal.forms import ImageAnnotationForm
from mezzanine.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext


###########################################################
### BONHUM - Rewriting of AllographSelect.render_option ###
###                                                     ###
### BEGINNING                                           ###
###########################################################

# MODIFICATIONS
# - added a custom attribute, 'is_story_character', which is 'true' if the
# allograph (motive) is linked to a story_character, 'false' otherwise;
# the value of the attribute is then used to filter the allographs (motives)

from digipal.forms import AllographSelect

def render_option(self, selected_choices, option_value, option_label):
    ret = super(AllographSelect, self).render_option(selected_choices, option_value, option_label)
    if option_value:
        a = Allograph.objects.get(id=int(option_value))
        type_id = a.character.ontograph.ontograph_type.id
        is_story_character = 'true' if hasattr(a, 'bonhum_motivestorycharacter') else 'false'
        ret = ret.replace(
            '<option ',
            '<option class="type-%s" is_story_character="%s" ' % (type_id, is_story_character)
        )
    return ret

AllographSelect.render_option = render_option

###########################################################
### END                                                 ###
###                                                     ###
### BONHUM - Rewriting of AllographSelect.render_option ###
###########################################################


##############################################
### BONHUM - Rewriting of annotation.image ###
###                                        ###
### BEGINNING                              ###
##############################################

# MODIFICATIONS
# - added labels for fields Hand (Type) and Allograph (Motive)
# - added the allographs (motives) related to the story_characters linked
# to the image to the list of allographs (motives)

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

    from digipal_project.models import Bonhum_MotiveStoryCharacter, Bonhum_ImageStoryCharacter

    # Get all the motives related to story_characters
    # - Bonhum_MotiveStoryCharacter inherits from Allograph and has only one property of its own: story_character
    # - 'story_character' refers to digipal_project.Bonhum_StoryCharacter
    # - 'character' refers to digipal.Character
    character_motives = Bonhum_MotiveStoryCharacter.objects.all().values('id', 'story_character__id', 'character__id')

    # Get all the relationships between the image and story_characters
    # - Bonhum_ImageStoryCharacter is an intermediary table between digipal.Image
    # and digipal_project.Bonhum_StoryCharacter
    # - 'story_character' refers to digipal_project.Bonhum_StoryCharacter
    # - 'category' refers to digipal.Character
    character_image_relations = Bonhum_ImageStoryCharacter.objects.filter(image__id=image_id).values('story_character__id', 'category__id')

    # For each relation between the image and a story_character,
    # we get the motive that matches the relation, ie story_character and category/character are the same
    related_character_motives_ids = []
    for relation in character_image_relations:
        for motive in character_motives:
            if motive['story_character__id'] == relation['story_character__id'] and motive['character__id'] == relation['category__id']:
                related_character_motives_ids.append(motive['id'])

    # The list of allographs (motives) in the annotator interface includes:
    # - all the allographs that are not linked to a story_character
    # - all the allographs that are linked to a story_character which is linked to the image
    from django.db.models import Q
    form.fields['allograph'].queryset = Allograph.objects.filter(
        Q(bonhum_motivestorycharacter__isnull=True) | Q(id__in=related_character_motives_ids)
    )

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
        ########
        # 'character_motives_ids': related_character_motives_ids
        ########
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

##############################################
### END                                    ###
###                                        ###
### BONHUM - Rewriting of annotation.image ###
##############################################
