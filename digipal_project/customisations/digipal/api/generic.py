import json
from digipal import utils
from digipal.api.generic import get_request_params


#################################################
### BONHUM - Rewriting of API.process_request ###
###                                           ###
### BEGINNING                                 ###
#################################################

# MODIFICATIONS
# - added digipal_project models to API.process_request method

from digipal.api.generic import API

@classmethod
def process_request(cls, request, content_type, selector):
    '''
        Process ALL requests on the API.
        request = a Django request object
        content_type = lower case version of a DigiPal model
        selector = a string that specify which records to work on
    '''
    ret = {'success': True, 'errors': [], 'results': []}

    method = request.GET.get('@method', request.META['REQUEST_METHOD'])
    is_get = method in ['GET']

    # special case for content_type='content_type'
    if content_type in ['content_type', 'content_type2']:
        return cls.get_all_content_types(content_type)

    # refusal if there is no permission for that operation
    if not cls.has_permission(content_type, method):
        ret = {'success': False, 'errors': ['%s method not permitted on %s' % (
            method.upper(), content_type)], 'results': []}
        return json.dumps(ret)

    # find the model
    model = None
    from digipal import models as models1
    # TODO: find a more generic way to include other apps than hard-coding
    # the name here
    from digipal_text import models as models2
    from digipal_project import models as models3
    for models in [models1, models2, models3]:
        for member in dir(models):
            if member.lower() == content_type:
                model = getattr(models, member)
                if hasattr(model, '_meta'):
                    break

    if not model:
        ret['success'] = False
        ret['errors'] = u'Content type not found (%s).' % content_type
    else:
        # filter the selection
        # filter from the selector passed in the web path
        filters = {}
        ids = cls.get_list_from_csv(selector)
        if ids:
            filters['id__in'] = ids

        # filters in the query string
        # for filter, value in request.REQUEST.iteritems():
        request_params = get_request_params(request)
        for filter, value in request_params.iteritems():
            if filter.startswith('_'):
                # a conditional filter _FIELD__OP=VALUE
                filter = filter[1:]
                if value.startswith('['):
                    value = value[1:-1].split(',')
                if filter.endswith('__isnull'):
                    # That's necessary otherwise '1' will be only partly
                    # understood by django: it will do an inner join
                    # depiste also doing a IS NULL!
                    value = utils.get_bool_from_string(value)
                filters[filter] = value

        # get the records
        records = model.objects.filter(**filters).distinct().order_by('id')

        ret['count'] = records.count()

        # limit the result set
        limit = int(request.GET.get('@limit', cls.DEFAULT_LIMIT))
        records = records[0:limit]

        # we refuse changes over the whole data set!
        if records.count() and not filters and not is_get:
            ret['success'] = False
            ret['errors'] = u'Modification of a all records is not supported.'
        else:
            fieldsets = [f for f in request_params.get(
                '@select', '').split(',') if f]

            # generate the results
            for record in records:
                ret['results'].append(cls.get_data_from_record(
                    record, request, fieldsets, method))

    ret = json.dumps(ret)

    return ret

API.process_request = process_request

#################################################
### END                                       ###
###                                           ###
### BONHUM - Rewriting of API.process_request ###
#################################################
