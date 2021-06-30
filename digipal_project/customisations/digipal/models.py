from django.db import models
from django.utils.html import escape
from django.utils.safestring import mark_safe
from digipal.models import OntographType, Ontograph, CharacterForm, Character, \
    Allograph, AllographComponent, Text, CurrentItem, Person, Scribe, \
    Idiograph, IdiographComponent, ItemPart, Image, Hand, Graph
from mezzanine.conf import settings



#################################################
### BONHUM - Rewriting of class OntographType ###
###                                           ###
### BEGINNING                                 ###
#################################################

# MODIFICATIONS
# - added verbose_name in class Meta
# - added verbose_name_plural in class Meta

OntographType._meta.verbose_name = 'macro category type'
OntographType._meta.verbose_name_plural = 'macro category types'

#################################################
### END                                       ###
###                                           ###
### BONHUM - Rewriting of class OntographType ###
#################################################


#############################################
### BONHUM - Rewriting of class Ontograph ###
###                                       ###
### BEGINNING                             ###
#############################################

# MODIFICATIONS
# - changed help_text of field nesting_level
# - added verbose_name in class Meta
# - added verbose_name_plural in class Meta

Ontograph._meta.verbose_name = 'macro category'
Ontograph._meta.verbose_name_plural = 'macro categories'

Ontograph._meta.get_field('nesting_level').help_text = 'A macro category can contain another macro category of a higher level. E.g. level 3 con be made of macro categories of level 4 and above. Set 0 to prevent any nesting.'

#############################################
### END                                   ###
###                                       ###
### BONHUM - Rewriting of class Ontograph ###
#############################################


#################################################
### BONHUM - Rewriting of class CharacterForm ###
###                                           ###
### BEGINNING                                 ###
#################################################

# MODIFICATIONS
# - added a field 'created'
# - added a field 'modified'
# - added verbose_name in class Meta
# - added verbose_name_plural in class Meta

CharacterForm._meta.verbose_name = 'category form'
CharacterForm._meta.verbose_name_plural = 'category forms'

CharacterForm.add_to_class('created', models.DateTimeField(auto_now_add=True, editable=False))
CharacterForm.add_to_class('modified', models.DateTimeField(auto_now=True, editable=False))

#################################################
### END                                       ###
###                                           ###
### BONHUM - Rewriting of class CharacterForm ###
#################################################


#############################################
### BONHUM - Rewriting of class Character ###
###                                       ###
### BEGINNING                             ###
#############################################

# MODIFICATIONS
# - added verbose_name in class Meta
# - added verbose_name_plural in class Meta
# - added verbose_name to field ontograph

Character._meta.verbose_name = 'category'
Character._meta.verbose_name_plural = 'categories'

Character._meta.get_field('ontograph').verbose_name = 'macro category'

#############################################
### END                                   ###
###                                       ###
### BONHUM - Rewriting of class Character ###
#############################################


#############################################
### BONHUM - Rewriting of class Allograph ###
###                                       ###
### BEGINNING                             ###
#############################################

# MODIFICATIONS
# - added verbose_name in class Meta
# - added verbose_name_plural in class Meta
# - added verbose_name to field character
# - changed help_text of field hidden

Allograph._meta.verbose_name = 'motive'
Allograph._meta.verbose_name_plural = 'motives'

Allograph._meta.get_field('character').verbose_name = 'category'
Allograph._meta.get_field('hidden').help_text = 'If ticked the public users won\'t see this motive on the web site.'

#############################################
### END                                   ###
###                                       ###
### BONHUM - Rewriting of class Allograph ###
#############################################


######################################################
### BONHUM - Rewriting of class AllographComponent ###
###                                                ###
### BEGINNING                                      ###
######################################################

# MODIFICATIONS
# - added verbose_name in class Meta
# - added verbose_name_plural in class Meta

AllographComponent._meta.verbose_name = 'motive component'
AllographComponent._meta.verbose_name_plural = 'motive components'

######################################################
### END                                            ###
###                                                ###
### BONHUM - Rewriting of class AllographComponent ###
######################################################


########################################
### BONHUM - Rewriting of class Text ###
###                                  ###
### BEGINNING                        ###
########################################

# MODIFICATIONS
# - changed ordering in class Meta
# - changed verbose_name in class Meta
# - changed verbose_name_plural in class Meta
# - deleted unique_together in class Meta
# - changed method __unicode__
# - added fields: title, reference, type, item_part, edition, mythological,
# story_start_date, story_place, story_characters, images, sources, collaborators
# - added methods: clean, validate_unique, save, get_itempart_work, get_itempart_currentitem, get_edition_work, get_first_image

Text._meta.verbose_name = 'text'
Text._meta.verbose_name_plural = 'texts'
Text._meta.ordering = ['title']
Text._meta.unique_together = []

Text.add_to_class('title', models.TextField(null=False, default=''))
Text.add_to_class('reference', models.CharField(max_length=30, verbose_name='canonical reference', null=False, default=''))
Text.add_to_class('type', models.ForeignKey('digipal_project.Bonhum_TextType', null=True, blank=False))
Text.add_to_class('item_part', models.ForeignKey('ItemPart', blank=True, null=True, default=None, help_text='Please select either an item part or an edition.'))
Text.add_to_class('edition', models.ForeignKey('digipal_project.Bonhum_Edition', blank=True, null=True, default=None, help_text='Please select either an item part or an edition.'))
Text.add_to_class('mythological', models.BooleanField(default=False))
Text.add_to_class('story_start_date', models.CharField(max_length=30, blank=True, null=True, help_text='Only if the story is not mythological.'))
Text.add_to_class('story_place', models.ForeignKey('digipal_project.Bonhum_StoryPlace', blank=True, null=True, default=None))
Text.add_to_class('story_characters', models.ManyToManyField('digipal_project.Bonhum_StoryCharacter', through='digipal_project.Bonhum_TextStoryCharacter', related_name='story_characters_of_text'))
Text.add_to_class('images', models.ManyToManyField('Image', through='digipal_project.Bonhum_TextImage', related_name='images_of_text'))
Text.add_to_class('sources', models.ManyToManyField('digipal_project.Bonhum_Source', through='digipal_project.Bonhum_TextSource', related_name='sources_of_text'))
Text.add_to_class('collaborators', models.ManyToManyField('digipal_project.Bonhum_Collaborator', through='digipal_project.Bonhum_TextCollaborator', related_name='collaborators_of_text'))


def __unicode__(self):
    return u'%s' % self.title

Text.__unicode__ = __unicode__


def validate_unique(self, exclude=None):
    super(Text, self).validate_unique(exclude)
    from django.core.exceptions import ValidationError
    if self.reference and self.item_part:
        if Text.objects.filter(reference=self.reference, item_part=self.item_part).exclude(id=self.id).exists():
            errors = {}
            errors.setdefault('reference', []).append(ur'Text with this canonical reference and this item part already exists.')
            raise ValidationError(errors)
    elif self.reference and self.edition:
        if Text.objects.filter(reference=self.reference, edition=self.edition).exclude(id=self.id).exists():
            errors = {}
            errors.setdefault('reference', []).append(ur'Text with this canonical reference and this edition already exists.')
            raise ValidationError(errors)

Text.validate_unique = validate_unique


def clean(self):
    from django.core.exceptions import ValidationError
    if (self.item_part is None and self.edition is None) or (self.item_part and self.edition):
        raise ValidationError('A text must refer to an Item Part or an Edition.')
    if self.mythological and self.story_start_date:
        raise ValidationError('A text can\'t be mythological and have a story start date.')

Text.clean = clean


def save(self, *args, **kwargs):
    self.name = self.title[:200]
    super(Text, self).save(*args, **kwargs)

Text.save = save


# If the text is related to an item part,
# returns the work this item part is from
def get_itempart_work(self):
    if self.item_part and self.item_part.work_current_item:
        return self.item_part.work_current_item.work
get_itempart_work.short_description = 'Work'

Text.get_itempart_work = get_itempart_work


# If the text is related to an item part,
# returns the current item this item part is from
def get_itempart_currentitem(self):
    if self.item_part and self.item_part.work_current_item:
        return self.item_part.work_current_item.current_item
get_itempart_currentitem.short_description = 'Current Item'

Text.get_itempart_currentitem = get_itempart_currentitem


# If the text is related to an edition,
# returns the work this item part is from
def get_edition_work(self):
    if self.edition:
        return self.edition.work
get_edition_work.short_description = 'Work'

Text.get_edition_work = get_edition_work


# Returns the first non private image for this text
# If in DEBUG mode permissions are ignored
def get_first_image(self):
    ret = Image.sort_query_set_by_locus(self.images.all())
    if not settings.DEBUG:
        ret = Image.filter_permissions(ret, [
            MediaPermission.PERM_PUBLIC, MediaPermission.PERM_THUMB_ONLY])
    return ret.first()

Text.get_first_image = get_first_image


########################################
### END                              ###
###                                  ###
### BONHUM - Rewriting of class Text ###
########################################


###############################################
### BONHUM - Rewriting of class CurrentItem ###
###                                         ###
### BEGINNING                               ###
###############################################

# MODIFICATIONS
# - added field works
# - added method get_item_parts

CurrentItem.add_to_class('works', models.ManyToManyField('digipal_project.Bonhum_Work', through='digipal_project.Bonhum_WorkCurrentItem', related_name='works_of_current_item'))


# Gets all the item parts related to this current item
# and returns a list of links
def get_item_parts(self):
    item_parts = []
    from django.db import connection
    condition = self.id
    if self.id:
        cursor = connection.cursor()
        select = u'''
                select ip.id, ip.display_label
                from digipal_itempart ip
                join digipal_project_bonhum_workcurrentitem wci
                on ip.work_current_item_id = wci.id
                where wci.current_item_id = %s
                ''' % condition
        cursor.execute(select)
        for item_part in list(cursor.fetchall()):
            item_parts.append(item_part)
        cursor.close()

    def get_item_part_with_link(item_part):
        url = u'/admin/digipal/itempart/%s/' % item_part[0]
        result = u'<tr><td><a href="%s" target="_blank">%s</a></td></tr>' % (escape(url), item_part[1])
        return result

    if len(item_parts) != 0:
        result = '<table>'
        for item_part in item_parts:
            result += get_item_part_with_link(item_part)
        result += '</table>'
        return mark_safe(result)
    return '(None)'
get_item_parts.short_description = 'Item parts'

CurrentItem.get_item_parts = get_item_parts

###############################################
### END                                     ###
###                                         ###
### BONHUM - Rewriting of class CurrentItem ###
###############################################


##########################################
### BONHUM - Rewriting of class Person ###
###                                    ###
### BEGINNING                          ###
##########################################

# MODIFICATIONS
# - added field sources
# - added field id_viaf
# - added methods get_viaf_url and get_viaf_url_with_link

Person.add_to_class('sources', models.ManyToManyField('digipal_project.Bonhum_Source', through='digipal_project.Bonhum_SourceAuthor', related_name='sources_of_person'))
Person.add_to_class('id_viaf', models.IntegerField(blank=True, null=True, verbose_name='VIAF identifier'))


def get_viaf_url(self):
    ret = u''
    if self.id_viaf:
        url = u'https://viaf.org/viaf/%s/' % self.id_viaf
        ret = escape(url)
    return ret

Person.get_viaf_url = get_viaf_url


def get_viaf_url_with_link(self):
    ret = u''
    if self.get_viaf_url():
        ret = u'<a href="%s" target="_blank">%s</a>' % (self.get_viaf_url(),
               'Link to the VIAF page of this person')
        ret = mark_safe(ret)
    return ret
get_viaf_url_with_link.short_description = 'VIAF link'

Person.get_viaf_url_with_link = get_viaf_url_with_link

##########################################
### END                                ###
###                                    ###
### BONHUM - Rewriting of class Person ###
##########################################


##########################################
### BONHUM - Rewriting of class Scribe ###
###                                    ###
### BEGINNING                          ###
##########################################

# MODIFICATIONS
# - added verbose_name in class Meta
# - added verbose_name_plural in class Meta
# - changed ordering in class Meta
# - added field type
# - added verbose_name to field scriptorium

Scribe._meta.verbose_name = 'contributor'
Scribe._meta.verbose_name_plural = 'contributors'
Scribe._meta.ordering = ['type', 'name']

Scribe._meta.get_field('scriptorium').verbose_name = 'workshop'

Scribe.add_to_class('type', models.ForeignKey('digipal_project.Bonhum_ContributorType', null=True, blank=False))

##########################################
### END                                ###
###                                    ###
### BONHUM - Rewriting of class Scribe ###
##########################################


#############################################
### BONHUM - Rewriting of class Idiograph ###
###                                       ###
### BEGINNING                             ###
#############################################

# MODIFICATIONS
# - added verbose_name in class Meta
# - added verbose_name_plural in class Meta
# - added verbose_name to field allograph
# - added verbose_name to field scribe
# - changed max_length of field display_label

Idiograph._meta.verbose_name = 'attribution'
Idiograph._meta.verbose_name_plural = 'attributions'

Idiograph._meta.get_field('allograph').verbose_name = 'motive'
Idiograph._meta.get_field('scribe').verbose_name = 'contributor'
Idiograph._meta.get_field('display_label').max_length = 518

#############################################
### END                                   ###
###                                       ###
### BONHUM - Rewriting of class Idiograph ###
#############################################


######################################################
### BONHUM - Rewriting of class IdiographComponent ###
###                                                ###
### BEGINNING                                      ###
######################################################

# MODIFICATIONS
# - added verbose_name in class Meta
# - added verbose_name_plural in class Meta

IdiographComponent._meta.verbose_name = 'attribution component'
IdiographComponent._meta.verbose_name_plural = 'attribution components'

######################################################
### END                                            ###
###                                                ###
### BONHUM - Rewriting of class IdiographComponent ###
######################################################


############################################
### BONHUM - Rewriting of class ItemPart ###
###                                      ###
### BEGINNING                            ###
############################################

# MODIFICATIONS
# - added field work_current_item
# - added methods: get_workcurrentitem_work, get_workcurrentitem_currentitem
# - changed help_text of field locus
# - changed method save

ItemPart._meta.get_field('locus').help_text = 'The location of this part in the current item.'

ItemPart.add_to_class('work_current_item', models.ForeignKey('digipal_project.Bonhum_WorkCurrentItem', verbose_name='current item/work', null=True, blank=False))


def save(self, *args, **kwargs):
    self._update_display_label()
    if (self.work_current_item):
        self.current_item = self.work_current_item.current_item
    super(ItemPart, self).save(*args, **kwargs)

ItemPart.save = save


def get_workcurrentitem_work(self):
    if self.work_current_item:
        return self.work_current_item.work
get_workcurrentitem_work.short_description = 'Work'

ItemPart.get_workcurrentitem_work = get_workcurrentitem_work


def get_workcurrentitem_currentitem(self):
    if self.work_current_item:
        return self.work_current_item.current_item
get_workcurrentitem_currentitem.short_description = 'Current Item'

ItemPart.get_workcurrentitem_currentitem = get_workcurrentitem_currentitem

############################################
### END                                  ###
###                                      ###
### BONHUM - Rewriting of class ItemPart ###
############################################


#########################################
### BONHUM - Rewriting of class Image ###
###                                   ###
### BEGINNING                         ###
#########################################

# MODIFICATIONS
# - added field texts
# - added field story_characters

Image.add_to_class('texts', models.ManyToManyField(Text, through='digipal_project.Bonhum_TextImage', related_name='texts_of_image'))
Image.add_to_class('story_characters', models.ManyToManyField('digipal_project.Bonhum_StoryCharacter', through='digipal_project.Bonhum_ImageStoryCharacter', related_name='story_characters_of_image'))

#########################################
### END                               ###
###                                   ###
### BONHUM - Rewriting of class Image ###
#########################################


########################################
### BONHUM - Rewriting of class Hand ###
###                                  ###
### BEGINNING                        ###
########################################

# MODIFICATIONS
# - added verbose_name to field scribe
# - made field scribe not nullable (in interface only)

Hand._meta.get_field('scribe').verbose_name = 'contributor'
Hand._meta.get_field('scribe').blank = False

########################################
### END                              ###
###                                  ###
### BONHUM - Rewriting of class Hand ###
########################################


#########################################
### BONHUM - Rewriting of class Graph ###
###                                   ###
### BEGINNING                         ###
#########################################

# MODIFICATIONS
# - added verbose_name to field idiograph
# - changed max_length of field display_label

Graph._meta.get_field('idiograph').verbose_name = 'attribution'
Graph._meta.get_field('display_label').max_length = 600

#########################################
### END                               ###
###                                   ###
### BONHUM - Rewriting of class Graph ###
#########################################
