from django.db import models
from digipal_text.models import TextContentType, TextContent, \
    TextContentXMLStatus, TextContentXMLCopy, TextContentXML


###################################################
### BONHUM - Rewriting of class TextContentType ###
###                                             ###
### BEGINNING                                   ###
###################################################

# MODIFICATIONS
# - changed verbose_name in class Meta
# - changed verbose_name_plural in class Meta

TextContentType._meta.verbose_name = 'Text content type'
TextContentType._meta.verbose_name_plural = 'Text content types'

###################################################
### END                                         ###
###                                             ###
### BONHUM - Rewriting of class TextContentType ###
###################################################


###############################################
### BONHUM - Rewriting of class TextContent ###
###                                         ###
### BEGINNING                               ###
###############################################

# MODIFICATIONS
# - changed verbose_name in class Meta
# - changed verbose_name_plural in class Meta
# - made field item_part nullable
# - added field edition
# - made field text mandatory in admin
# - removed unique_together
# - changed methods __unicode__ and get_absolute_url
# - added methods save and validate_unique

TextContent._meta.verbose_name = 'Text content (meta)'
TextContent._meta.verbose_name_plural = 'Text contents (meta)'

TextContent._meta.get_field('item_part').null = True
TextContent.add_to_class('edition', models.ForeignKey('digipal_project.Bonhum_Edition', null=True, related_name='text_contents'))

TextContent._meta.get_field('text').blank = False

TextContent._meta.unique_together = []


def __unicode__(self):
    ret = u'New TextContent record'
    if self.pk:
        info = unicode(self.type)
        languages = self.get_string_from_languages()
        if languages:
            info += u', %s' % languages
        if self.item_part:
            origin = self.item_part
        elif self.edition:
            origin = self.edition
        ret = u'%s (%s)' % (origin, info)
    return ret

TextContent.__unicode__ = __unicode__


def save(self, *args, **kwargs):
    from digipal_text.models import TextContentType
    if self.text and self.text.item_part:
        self.item_part = self.text.item_part
        self.type = TextContentType.objects.filter(slug='transcription').first()
    if self.text and self.text.edition:
        self.edition = self.text.edition
        self.type = TextContentType.objects.filter(slug='edited').first()
    super(TextContent, self).save(*args, **kwargs)

TextContent.save = save


def validate_unique(self, exclude=None):
    super(TextContent, self).validate_unique(exclude)
    from django.core.exceptions import ValidationError
    if self.text and self.text.item_part:
        if TextContent.objects.filter(text=self.text, type__slug='transcription', item_part=self.text.item_part).exclude(id=self.id).exists():
            errors = {}
            errors.setdefault('text', []).append(ur'A TextContent already exists for this text and this item part.')
            raise ValidationError(errors)
    if self.text and self.text.edition:
        if TextContent.objects.filter(text=self.text, type__slug='edited', edition=self.text.edition).exclude(id=self.id).exists():
            errors = {}
            errors.setdefault('text', []).append(ur'A TextContent already exists for this text and this edition.')
            raise ValidationError(errors)

TextContent.validate_unique = validate_unique


def get_absolute_url(self, unset=False, qs='', metas=None,
                     location_type=None, location=None, content_types=None):
    '''
        Returns the url to view this text content.
        unset: if True the panels types and content are unspecified
        qs: a partial query string to be added to the url
        metas: additional settings for the main panel (e.g. 'k1=v1;k2=v2')
        content_types: list of content_types (e.g. transcription) to display in the panels
    '''
    if self.item_part:
        types = (content_types or ['transcription'])
        ret = u'%stexts/%s/view/' % (self.item_part.get_absolute_url(), self.text.id)
    elif self.edition:
        types = (content_types or ['edited'])
        ret = u'%stexts/%s/view/' % (self.edition.get_absolute_url(), self.text.id)
    if not unset:
        if self.item_part:
            ret += '?' if ('?' not in ret) else '&'
            ret += 'center=%s/sync/location' % self.type.slug
            if 0 and location_type:
                ret += '/%s' % location_type
                if location:
                    ret += '/%s' % location
            if 0 and metas:
                from digipal.utils import urlencode
                ret += (';' + urlencode(metas, True)).replace('=', ':')
            ret += '&east=image/sync/location'
        elif self.edition:
            ret += '?' if ('?' not in ret) else '&'
            ret += 'center=%s/whole/' % self.type.slug
            if 0 and location_type:
                ret += '/%s' % location_type
                if location:
                    ret += '/%s' % location
            if 0 and metas:
                from digipal.utils import urlencode
                ret += (';' + urlencode(metas, True)).replace('=', ':')
    if location_type:
        ret += '?' if ('?' not in ret) else '&'
        ret += 'above=location/%s' % location_type
        if location:
            ret += '/%s' % location
        if metas:
            from digipal.utils import urlencode
            ret += (';' + urlencode(metas, True)).replace('=', ':')
    if qs:
        ret += '?' if ('?' not in ret) else '&'
        if qs[0] in ['&', '?']:
            qs = qs[1:]
        ret += qs
    return ret

TextContent.get_absolute_url = get_absolute_url


###############################################
### END                                     ###
###                                         ###
### BONHUM - Rewriting of class TextContent ###
###############################################


########################################################
### BONHUM - Rewriting of class TextContentXMLStatus ###
###                                                  ###
### BEGINNING                                        ###
########################################################

# MODIFICATIONS
# - changed verbose_name in class Meta
# - changed verbose_name_plural in class Meta

TextContentXMLStatus._meta.verbose_name = 'Text content status'
TextContentXMLStatus._meta.verbose_name_plural = 'Text content statuses'

########################################################
### END                                              ###
###                                                  ###
### BONHUM - Rewriting of class TextContentXMLStatus ###
########################################################


######################################################
### BONHUM - Rewriting of class TextContentXMLCopy ###
###                                                ###
### BEGINNING                                      ###
######################################################

# MODIFICATIONS
# - changed verbose_name in class Meta
# - changed verbose_name_plural in class Meta

TextContentXMLCopy._meta.verbose_name = 'Text content copy'
TextContentXMLCopy._meta.verbose_name_plural = 'Text content copies'

######################################################
### END                                            ###
###                                                ###
### BONHUM - Rewriting of class TextContentXMLCopy ###
######################################################


##################################################
### BONHUM - Rewriting of class TextContentXML ###
###                                            ###
### BEGINNING                                  ###
##################################################

# MODIFICATIONS
# - changed verbose_name in class Meta
# - changed verbose_name_plural in class Meta

TextContentXML._meta.verbose_name = 'Text content (XML)'
TextContentXML._meta.verbose_name_plural = 'Text contents (XML)'

##################################################
### END                                        ###
###                                            ###
### BONHUM - Rewriting of class TextContentXML ###
##################################################
