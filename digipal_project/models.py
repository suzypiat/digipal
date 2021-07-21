from django.db import models
from mezzanine.conf import settings
import os
from django.utils.html import escape
from django.utils.safestring import mark_safe
from digipal.models import Language, Text, Person, CurrentItem, ItemPart, Image, \
    Allograph, Character, Graph, get_list_as_string


def model_get_admin_url(self):
    from django.core.urlresolvers import reverse
    info = (self._meta.app_label, self._meta.model_name)
    ret = reverse('admin:%s_%s_change' % info, args=(self.pk,))
    return ret


#########################
#                       #
#   Story Place         #
#                       #
#########################

class Bonhum_StoryPlaceType(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    level = models.IntegerField(choices=((0,'0'),(1,'1'),(2,'2')), default=0,
            help_text='The level of this story place type:<br/>0 means a country, a river, an ocean, a mountain or a mythological place<br/>1 means a region<br/>2 means a city')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['level', 'name']
        unique_together = ['name', 'level']
        verbose_name = 'story place type'
        verbose_name_plural = 'story place types'

    def __unicode__(self):
        return u'%s' % self.name


class Bonhum_StoryPlaceNature(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'story place nature'
        verbose_name_plural = 'story place natures'

    def __unicode__(self):
        return u'%s' % self.name


class Bonhum_StoryPlace(models.Model):
    name = models.CharField(max_length=150, null=False)
    type = models.ForeignKey(Bonhum_StoryPlaceType, null=False)
    nature = models.ForeignKey(Bonhum_StoryPlaceNature, null=False)
    parent = models.ForeignKey('self', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'parent']
        verbose_name = 'story place'
        verbose_name_plural = 'story places'

    def __unicode__(self):
        return u'%s' % self.name

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.parent and (self.nature.name.lower() != 'mythologique' and self.type.level != 0):
            raise ValidationError('A story place whose nature is not \'mythological\' and whose type level is not 0 must have a parent.')
        if self.parent and (self.nature.name.lower() == 'mythologique' or self.type.level == 0):
            raise ValidationError('A story place whose nature is \'mythological\' or whose type level is 0 can\'t have a parent.')
        if self.parent and self.parent.type.level != self.type.level - 1:
            raise ValidationError('A story place parent must have a direct inferior type level.')

    def get_absolute_url(self):
        ret = '/%s/%s/%s/' % ('digipal', 'places', self.id)
        return ret

    def get_admin_url(self):
        return model_get_admin_url(self)


class Bonhum_StoryPlaceNameVariant(models.Model):
    name = models.CharField(max_length=150, null=False)
    place = models.ForeignKey(Bonhum_StoryPlace, null=False)
    language = models.ForeignKey(Language, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'place', 'language']
        verbose_name = 'story place name variant'
        verbose_name_plural = 'story place name variants'

    def __unicode__(self):
        return get_list_as_string(self.name, ' - ', self.language)


#########################
#                       #
#   Story Character     #
#                       #
#########################

class Bonhum_StoryCharacterAge(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'character age'
        verbose_name_plural = 'character ages'

    def __unicode__(self):
        return u'%s' % self.name


class Bonhum_StoryCharacterGender(models.Model):
    name = models.CharField(max_length=15, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'character gender'
        verbose_name_plural = 'character genders'

    def __unicode__(self):
        return u'%s' % self.name


class Bonhum_StoryCharacterType(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'character type'
        verbose_name_plural = 'character types'

    def __unicode__(self):
        return u'%s' % self.name


class Bonhum_StoryCharacterReligion(models.Model):
    name = models.CharField(max_length=60, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'character religion'
        verbose_name_plural = 'character religions'

    def __unicode__(self):
        return u'%s' % self.name


class Bonhum_StoryCharacterTitle(models.Model):
    name = models.CharField(max_length=45, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'character title'
        verbose_name_plural = 'character titles'

    def __unicode__(self):
        return u'%s' % self.name


class Bonhum_StoryCharacterOccupation(models.Model):
    name = models.CharField(max_length=45, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'character occupation'
        verbose_name_plural = 'character occupations'

    def __unicode__(self):
        return u'%s' % self.name


class Bonhum_StoryCharacterTrait(models.Model):
    name = models.CharField(max_length=45, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'character trait'
        verbose_name_plural = 'character traits'

    def __unicode__(self):
        return u'%s' % self.name


class Bonhum_StoryCharacter(models.Model):
    name = models.CharField(max_length=150, null=False, unique=True)
    id_viaf = models.IntegerField(blank=True, null=True, verbose_name='VIAF identifier')
    type = models.ForeignKey(Bonhum_StoryCharacterType, blank=True, null=True)
    gender = models.ForeignKey(Bonhum_StoryCharacterGender, blank=True, null=True)
    age = models.ForeignKey(Bonhum_StoryCharacterAge, blank=True, null=True)
    religion = models.ForeignKey(Bonhum_StoryCharacterReligion, blank=True, null=True)
    geographical_origin = models.ForeignKey(Bonhum_StoryPlace, blank=True, null=True)
    occupations = models.ManyToManyField(Bonhum_StoryCharacterOccupation, blank=True)
    titles = models.ManyToManyField(Bonhum_StoryCharacterTitle, blank=True)
    traits = models.ManyToManyField(Bonhum_StoryCharacterTrait, blank=True)
    texts = models.ManyToManyField(Text, through='Bonhum_TextStoryCharacter', related_name='texts_of_story_character')
    images = models.ManyToManyField(Image, through='Bonhum_ImageStoryCharacter', related_name='images_of_story_character')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'character'
        verbose_name_plural = 'characters'

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        ret = '/%s/%s/%s/' % ('digipal', 'characters', self.id)
        return ret

    def get_admin_url(self):
        return model_get_admin_url(self)

    def get_graphs(self):
        motives_ids = Bonhum_MotiveStoryCharacter.objects.filter(story_character__id=self.id).values_list('id')
        graphs = Graph.objects.filter(idiograph__allograph__id__in=motives_ids)
        return graphs

    def get_thumbnail(self, request=None):
        graphs = self.get_graphs()
        ret = graphs.first().annotation if len(graphs) > 0 else None
        # returns None if request user doesn't have permission
        if request and ret and ret.image.is_private_for_user(request):
            ret = None
        return ret

    def get_viaf_url(self):
        ret = u''
        if self.id_viaf:
            url = u'https://viaf.org/viaf/%s/' % self.id_viaf
            ret = escape(url)
        return ret

    def get_viaf_url_with_link(self):
        ret = u''
        if self.get_viaf_url():
            ret = u'<a href="%s" target="_blank">%s</a>' % (self.get_viaf_url(),
                   'Link to the VIAF page of this character')
            ret = mark_safe(ret)
        return ret
    get_viaf_url_with_link.short_description = 'VIAF link'


class Bonhum_MotiveStoryCharacter(Allograph):
    story_character = models.ForeignKey(Bonhum_StoryCharacter, null=False)

    def __unicode__(self):
        return get_list_as_string(self.character, ', ', self.name)


class Bonhum_ImageStoryCharacter(models.Model):
    image = models.ForeignKey(Image, null=False)
    story_character = models.ForeignKey(Bonhum_StoryCharacter, null=False, verbose_name='character')
    category = models.ForeignKey(Character, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ['image', 'story_character', 'category']
        verbose_name = 'image-character relationship'
        verbose_name_plural = 'image-character relationships'

    def __unicode__(self):
        return get_list_as_string(self.image, '/', self.story_character)

    def save(self, *args, **kwargs):
        if self.story_character and self.category:
            story_character = Bonhum_StoryCharacter.objects.filter(id=self.story_character.id).first()
            motive, created = Bonhum_MotiveStoryCharacter.objects.get_or_create(
                story_character=self.story_character, character=self.category,
                defaults={ 'name': story_character.name }
            )
        super(Bonhum_ImageStoryCharacter, self).save(*args, **kwargs)


class Bonhum_TextStoryCharacter(models.Model):
    text = models.ForeignKey(Text, null=False)
    story_character = models.ForeignKey(Bonhum_StoryCharacter, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ['text', 'story_character']
        verbose_name = 'text-character relationship'
        verbose_name_plural = 'text-character relationships'

    def __unicode__(self):
        return get_list_as_string(self.text, '/', self.story_character)


class Bonhum_StoryCharacterNameVariant(models.Model):
    name = models.CharField(max_length=150, null=False)
    character = models.ForeignKey(Bonhum_StoryCharacter, null=False)
    language = models.ForeignKey(Language, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'character', 'language']
        verbose_name = 'character name variant'
        verbose_name_plural = 'character name variants'

    def __unicode__(self):
        return get_list_as_string(self.name, ' - ', self.language)


#########################
#                       #
#   Source              #
#   Work                #
#   Edition             #
#   Text                #
#                       #
#########################


class Bonhum_SourceType(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'source type'
        verbose_name_plural = 'source types'

    def __unicode__(self):
        return u'%s' % self.name


class Bonhum_Source(models.Model):
    title = models.TextField(null=False)
    reference = models.TextField(verbose_name='canonical reference', null=False, unique=True)
    type = models.ForeignKey(Bonhum_SourceType, null=False)
    authors = models.ManyToManyField(Person, through='Bonhum_SourceAuthor', related_name='authors_of_source')
    texts = models.ManyToManyField(Text, through='Bonhum_TextSource', related_name='texts_of_source')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['title']
        verbose_name = 'source'
        verbose_name_plural = 'sources'

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        ret = '/%s/%s/%s/' % ('digipal', 'sources', self.id)
        return ret

    def get_admin_url(self):
        return model_get_admin_url(self)


class Bonhum_SourceAuthor(models.Model):
    source = models.ForeignKey(Bonhum_Source, null=False)
    author = models.ForeignKey(Person, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ['source', 'author']
        verbose_name = 'source-author relationship'
        verbose_name_plural = 'source-author relationships'

    def __unicode__(self):
        return get_list_as_string(self.source, '/', self.author)


class Bonhum_TextType(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'text type'
        verbose_name_plural = 'text types'

    def __unicode__(self):
        return u'%s' % self.name


class Bonhum_TextSource(models.Model):
    source = models.ForeignKey(Bonhum_Source, null=False)
    text = models.ForeignKey(Text, null=False)
    canonical_reference = models.CharField(max_length=25, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ['source', 'text', 'canonical_reference']
        verbose_name = 'text-source relationship'
        verbose_name_plural = 'text-source relationships'

    def __unicode__(self):
        return get_list_as_string(self.source, '/', self.text)


class Bonhum_Work(models.Model):
    title = models.TextField(null=False)
    date = models.CharField(max_length=30, null=False)
    language = models.ForeignKey(Language, null=False)
    original_version = models.BooleanField(default=False)
    current_items = models.ManyToManyField(CurrentItem, through='Bonhum_WorkCurrentItem', related_name='current_items_of_work')
    translator = models.ForeignKey(Person, blank=True, null=True, help_text='A translator must be selected if it is not an original version.')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['title']
        unique_together = ['title', 'date']
        verbose_name = 'work'
        verbose_name_plural = 'works'

    def __unicode__(self):
        return u'%s' % self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.original_version and self.translator:
            raise ValidationError('A work in original version can\'t have a translator.')
        if not self.original_version and self.translator is None:
            raise ValidationError('A work not in original version must have a translator.')

    # Gets all the texts related to this work through an edition
    # and returns a list of links
    def get_texts_by_edition(self):
        editions_ids = Bonhum_Edition.objects.filter(work_id=self.id).values_list('id')
        texts = Text.objects.filter(edition_id__in=editions_ids)

        def get_text_with_link(text):
            url = u'/admin/digipal/text/%s/' % text.id
            result = u'<tr><td><a href="%s" target="_blank">%s, %s</a></td></tr>' % (escape(url), text.reference, text.title)
            return result

        if len(texts) != 0:
            result = '<table>'
            for text in texts:
                result += get_text_with_link(text)
            result += '</table>'
            return mark_safe(result)
        return '(None)'
    get_texts_by_edition.short_description = 'By edition'

    # Gets all the texts related to this work through an item part
    # and returns a list of links
    def get_texts_by_item_part(self):
        int_table_ids = Bonhum_WorkCurrentItem.objects.filter(work_id=self.id).values_list('id')
        item_parts_ids = ItemPart.objects.filter(work_current_item_id__in=int_table_ids).values_list('id')
        texts = Text.objects.filter(item_part_id__in=item_parts_ids)

        def get_text_with_link(text):
            url = u'/admin/digipal/text/%s/' % text.id
            result = u'<tr><td><a href="%s" target="_blank">%s, %s</a></td></tr>' % (escape(url), text.reference, text.title)
            return result

        if len(texts) != 0:
            result = '<table>'
            for text in texts:
                result += get_text_with_link(text)
            result += '</table>'
            return mark_safe(result)
        return '(None)'
    get_texts_by_item_part.short_description = 'By item part'

    # Gets all the item parts (with their current item) related to this work
    # and returns a list of links
    def get_item_parts(self):
        int_table_ids = Bonhum_WorkCurrentItem.objects.filter(work_id=self.id).values_list('id')
        item_parts = ItemPart.objects.filter(work_current_item_id__in=int_table_ids)
        for item_part in item_parts:
            item_part.current_item = CurrentItem.objects.get(id=item_part.work_current_item.current_item_id)

        def get_item_part_with_link(item_part):
            url_item_part = u'/admin/digipal/itempart/%s/' % item_part.id
            url_current_item = u'/admin/digipal/currentitem/%s/' % item_part.current_item.id
            result = u'<tr><td><a href="%s" target="_blank">%s</a></td><td><a href="%s" target=blank>%s</a></td></tr>' % (escape(url_item_part),
                        item_part.display_label, escape(url_current_item), item_part.current_item.display_label)
            return result

        if len(item_parts) != 0:
            result = '<table>'
            for item_part in item_parts:
                result += get_item_part_with_link(item_part)
            result += '</table>'
            return mark_safe(result)
        return '(None)'
    get_item_parts.short_description = 'Item parts and their current item'


class Bonhum_WorkCurrentItem(models.Model):
    work = models.ForeignKey(Bonhum_Work, null=False)
    current_item = models.ForeignKey(CurrentItem, null=False)
    complete_work = models.BooleanField(default=False)
    work_title = models.TextField(blank=True, null=True, help_text='If the work name is different in this current item.')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['work', 'current_item']
        unique_together = ['work', 'current_item']
        verbose_name = 'current item-work relationship'
        verbose_name_plural = 'current item-work relationships'

    def __unicode__(self):
        return get_list_as_string(self.current_item, ' - ', self.work)


class Bonhum_Edition(models.Model):
    title = models.TextField(null=False, unique=True)
    editor = models.ForeignKey(Person, null=False)
    date = models.CharField(max_length=30, null=False)
    publisher = models.CharField(max_length=100, null=False)
    work = models.ForeignKey(Bonhum_Work, null=False)
    complete_work = models.BooleanField(default=False)
    work_title = models.TextField(blank=True, null=True, help_text='If the work name is different in this edition.')
    comments = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['title']
        verbose_name = 'edition'
        verbose_name_plural = 'editions'

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        ret = '/%s/%s/%s/' % ('digipal', 'editions', self.id)
        return ret


class Bonhum_TextImage(models.Model):
    text = models.ForeignKey(Text, null=False)
    image = models.ForeignKey(Image, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ['text', 'image']

    def __unicode__(self):
        return get_list_as_string(self.text, '/', self.image)


class Bonhum_Activity(models.Model):
    name = models.CharField(max_length=60, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'activity'
        verbose_name_plural = 'activities'

    def __unicode__(self):
        return u'%s' % self.name


class Bonhum_Collaborator(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    institution = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=255, null=False, unique=True)
    texts = models.ManyToManyField(Text, through='Bonhum_TextCollaborator', related_name='texts_of_collaborator')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = ['first_name', 'last_name']
        verbose_name = 'collaborator'
        verbose_name_plural = 'collaborators'

    def __unicode__(self):
        return get_list_as_string(self.first_name, ' ', self.last_name)


class Bonhum_TextCollaborator(models.Model):
    text = models.ForeignKey(Text, null=False)
    collaborator = models.ForeignKey(Bonhum_Collaborator, null=False)
    activity = models.ForeignKey(Bonhum_Activity, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['text']
        unique_together = ['text', 'collaborator', 'activity']
        verbose_name = 'text-collaborator relationship'
        verbose_name_plural = 'text-collaborator relationships'

    def __unicode__(self):
        return get_list_as_string(self.text, ' - ', self.collaborator, ', ', self.activity)


#########################
#                       #
#   Contributor         #
#                       #
#########################


class Bonhum_ContributorType(models.Model):
    name = models.CharField(max_length=15, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'contributor type'
        verbose_name_plural = 'contributor types'

    def __unicode__(self):
        return u'%s' % self.name


#########################
#                       #
#   Catalogue           #
#                       #
#########################


class Bonhum_Catalogue(models.Model):
    reference = models.TextField(null=False, unique=True)
    current_item = models.ForeignKey(CurrentItem, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['current_item', 'reference']
        unique_together = ['current_item', 'reference']
        verbose_name = 'catalogue'
        verbose_name_plural = 'catalogues'

    def __unicode__(self):
        return u'%s' % self.reference


# LEAVE THIS CALL, this is to make sure the customisations are loaded
os.path.basename(settings.PROJECT_ROOT)
module_path = os.path.basename(
    settings.PROJECT_ROOT) + '.customisations.digipal_project.models'
from importlib import import_module
try:
    import_module(module_path)
except ImportError as e:
    # Ingore, customisations are optional
    pass
