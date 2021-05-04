from digipal_text.models import TextContentType, TextContent, \
    TextContentXMLStatus, TextContentXML


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

TextContent._meta.verbose_name = 'Text content (meta)'
TextContent._meta.verbose_name_plural = 'Text contents (meta)'

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
