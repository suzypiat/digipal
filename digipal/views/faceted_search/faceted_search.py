from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
import json
from digipal.models import Image, Graph
from digipal.forms import SearchPageForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from digipal.templatetags import hand_filters, html_escape
from digipal import utils
from django.utils.datastructures import SortedDict

import logging
dplog = logging.getLogger('digipal_debugger')

class FacetedModel(object):
    
    def __init__(self, options):
        self.options = options
    
    def get_label(self):
        return self.options['label']
    label = property(get_label)

    def get_key(self):
        return self.options['key']
    key = property(get_key)
    
    def get_fields(self):
        return self.options['fields']
    fields = property(get_fields)
    
    def get_model(self):
        return self.options['model']
    model = property(get_model)

    def get_option(self, option_name, default=None):
        return self.options.get(option_name, default)
    
    def get_views(self):
        return self.get_option('views', [])
    views = property(get_views)
    
    def get_selected_views_template(self):
        for view in self.views:
            if view.get('selected', False):
                ret = view.get('key', 'table')
                break
        
        return 'search/faceted/views/' + ret + '.html' 
    selected_view_template = property(get_selected_views_template)

    def get_all_records(self, prefetch=False):
        ret = self.model.objects.filter(**self.get_option('django_filter', {}))
        if self.get_option('select_related'):
            ret = ret.select_related(*self.get_option('select_related'))
        if self.get_option('prefetch_related'):
            ret = ret.prefetch_related(*self.get_option('prefetch_related'))
        
        return ret
    
    @classmethod
    def _get_sortable_whoosh_field(cls, field):
        '''Returns the name of the whoosh field that we can use to sort the given field
            Returns None if field is not sortable
        '''
        ret = None
        
        if field and cls.is_field_indexable(field) and field.get('viewable', False):
            ret = field['key']
            if field['type'] in ['id', 'code', 'title']:
                ret += '_sortable'
                
        return ret
    
    def prepare_value_rankings(self):
        ''' populate self.value_rankings dict
            It generates a ranking number for each value in each sortable field 
            This will be stored in the index as a separate field to allow sorting by any column
        '''
        self.value_rankings = {}
        
        records = self.get_all_records(True)
        
        for field in self.fields:
            if self.is_field_indexable(field):
                whoosh_sortable_field = self._get_sortable_whoosh_field(field)
                if whoosh_sortable_field and whoosh_sortable_field != field['key']:
                    
                    print '\t\t'+field['key'], records.count()
                    
                    # get all the values for that field in the table
                    value_rankings = self.value_rankings[whoosh_sortable_field] = {}
                    for record in records:
                        value = self.get_record_field_whoosh(record, field)
                        value_rankings[value] = value or u''
                    
                    # sort with natural order
                    sorted_values = utils.sorted_natural(value_rankings.values(), True)
                    
                    # now assign the ranking to each value
                    for value in value_rankings.keys():
                        value_rankings[value] = sorted_values.index(value or u'')
                        
                    #print self.value_rankings[whoosh_sortable_field]
        
    def get_document_from_record(self, record):
        ret = {'id': u'%s' % record.id}
        for field in self.fields:
            if self.is_field_indexable(field):
                ret[field['key']] = self.get_record_field_whoosh(record, field)
                
                whoosh_sortable_field = self._get_sortable_whoosh_field(field)
                if whoosh_sortable_field and whoosh_sortable_field != field['key']:
                    ret[whoosh_sortable_field] = self.value_rankings[whoosh_sortable_field][ret[field['key']]]
                
                if field['type'] == 'date':
                    from digipal.utils import get_range_from_date, is_max_date_range
                    rng = get_range_from_date(ret[field['key']])
                    ret[field['key']+'_min'] = rng[0]
                    ret[field['key']+'_max'] = rng[1]
                    if is_max_date_range(rng): 
                        # we don't want the empty dates and invalid dates to be found
                        ret[field['key']+'_max'] = ret[field['key']+'_min']
                        
        return ret

    def get_field_by_key(self, key):
        # todo: think about caching this
        for field in self.fields:
            if field['key'] == key: 
                return field
        return None

    def get_filter_field_keys(self):
        ''' Returns a list of fields keys in the order they should appear in the filter panel '''
        ret = self.get_option('filter_order', None)
        if ret is None:
            ret = [field['key'] for field in self.fields if field.get('count', False) or field.get('filter', False)]
        return ret
    filter_field_keys = property(get_filter_field_keys)

    def get_facets(self, request):
        ret = []
        
        # a filter for search phrase 
        phrase_facet = {'label': 'Phrase', 'type': 'textbox', 'key': 'search_terms', 'value': request.GET.get('search_terms', ''), 'id': 'search-terms', 'selected_options': []}
        if phrase_facet['value']:
            phrase_facet['selected_options'] = [{'label': phrase_facet['value'], 'key': phrase_facet['value'], 'count': '?', 'selected': True}]
        ret.append(phrase_facet)
        
        # facets based on faceted fields
        from copy import deepcopy
        for key in self.filter_field_keys:
            field = self.get_field_by_key(key)
            facet = deepcopy(field)
            facet['options'] = self.get_facet_options(field, request)
            facet['value'] = request.GET.get(field['key'], '')
            
            if facet['value'] and field['type'] == 'date':
                from digipal.utils import get_range_from_date
                facet['values'] = get_range_from_date(facet['value'])
            
            facet['selected_options'] = []
            if facet['options']:
                facet['selected_options'] = [o for o in facet['options'] if o['selected']]
            else:
                if facet['value']:
                    facet['selected_options'] = [{'label': facet['value'], 'key': facet['value'], 'count': '?', 'selected': True}]
            ret.append(facet)
        return ret

    def get_facet_options(self, field, request):
        ret = []
        if not field.get('count', False):
            return ret
        selected_key = request.GET.get(field['key'], '')
        for k, v in self.whoosh_groups[field['key']].iteritems():
            ret.append({'key': k, 'label': k, 'count': v, 'selected': (selected_key == k) and (k)})
        ret = sorted(ret, key=lambda o: o['key'])
        return ret      
    
    def get_record_field_html(self, record, field_key):
        if not hasattr(field_key, 'get'):
            for field in self.fields:
                if field['key'] == field_key:
                    break
        
        ret = self.get_record_field(record, field)
        if field['type'] == 'url':
            ret = '<a href="%s" class="view_button">View</a>' % ret
        if field['type'] == 'image':
            # TODO: max_size as an argument for iip_img_a
            ret = html_escape.iip_img(ret, width=field.get('max_size', 50), lazy=1)
            
        if ret is None:
            ret = ''
            
        return ret
        
    def get_record_field_whoosh(self, record, afield):
        ret = self.get_record_field(record, afield)
        if ret is not None:
            ret = unicode(ret)
        
        return ret

    def get_record_field(self, record, afield):
        '''
            returns the value of record.afield 
            where record is a model instance and afield is field name.
            afield and go through related objects.
            afield can also be a field definition (e.g. self.fields[0]).
            afield can also be a function of the object.
        '''
        # split the path
        path = afield['path']
        v = record
        if path:
            from django.core.exceptions import ObjectDoesNotExist
            for part in path.split('.'):
#                 if not hasattr(v, part):
#                     message = u'2Model path error: %s : %s, \'%s\' not found' % (self.key, path, part)
#                     #raise Exception(message)
#                     print message
#                     v = getattr(v, part)
                try:
                    v = getattr(v, part)
                except ObjectDoesNotExist, e:
                    v = None
                except Exception, e:
                    raise Exception(u'Model path error: %s : %s, \'%s\' not found' % (self.key, path, part))
                                    
                if v is None:
                    break
                if callable(v):
                    v = v()
            
        ret = v

        return ret  

    def get_summary(self, request):
        ret = u''
        for facet in self.get_facets(request):
            for option in facet['selected_options']:
                href = html_escape.update_query_params('?'+request.META['QUERY_STRING'], {'page': [1], facet['key']: []})
                ret += u'<a href="%s" title="%s = \'%s\'" data-toggle="tooltip"><span class="label label-default">%s</span></a>' % (href, facet['label'], option['label'], option['label']) 

        from django.utils.safestring import mark_safe
        
        if not ret.strip():
            ret = 'All' 
            
        return mark_safe(ret)

    def get_columns(self):
        ret = []
        keys = self.get_option('column_order', None)
        if keys is None:
            ret = [field for field in self.fields if field.get('viewable', False)]
        else:
            ret = [self.get_field_by_key(key) for key in keys]
        for field in ret:
            field['sortable'] = self._get_sortable_whoosh_field(field)
            
        return ret
    
    def get_whoosh_facets(self):
        from whoosh import sorting
        print [field['key'] for field in self.fields if field.get('count', False)]
        return [sorting.StoredFieldFacet(field['key'], maptype=sorting.Count) for field in self.fields if field.get('count', False)]
    
    @classmethod
    def is_field_indexable(cls, field):
        return field.get('search', False) or field.get('count', False) or field.get('filter', False)
    
    def get_whoosh_sortedby(self, request):
        from whoosh import sorting
        return [sorting.FieldFacet(field, reverse=False) for field in self.get_sorted_fields_from_request(request, True)]
    
    def get_sorted_fields_from_request(self, request, whoosh_fields=False):
        '''Returns a list of field keys to sort by.
            e.g. ('repo_city', 'repo_place')
            The list will combine the sort fields from the request with the default sort fields.
            E.g. request ('c', 'd'); default is ('a', 'b', 'c') => ('c', 'd', 'a', 'b')
            
            if whoosh_fields is True, returns the whoosh_field keys, e.g. ('a_sortable', 'b')
        '''
        ret = self.get_option('sorted_fields', [])[:]
        for field in request.GET.get('sort', '').split(','):
            field = field.strip()
            if field and self._get_sortable_whoosh_field(self.get_field_by_key(field)):
                if field in ret: 
                    ret.remove(field)
                ret.insert(0, field)
                
        if whoosh_fields:
            ret = [self._get_sortable_whoosh_field(self.get_field_by_key(field)) for field in ret]
                
        return ret    
    
    def get_requested_records(self, request):
        selected = False
        selected_view_key = request.GET.get('view', '')
        if selected_view_key:
            for view in self.views:
                if view['key'] == selected_view_key:
                    view['selected'] = True
                    selected = True
                    break
        if self.views and not selected:
            self.views[0]['selected'] = True
        
        # run the query with Whoosh
        # 
        from whoosh.index import open_dir
        import os
        index = open_dir(os.path.join(settings.SEARCH_INDEX_PATH, 'faceted', self.key))

        #from whoosh.qparser import QueryParser
        
        search_phrase = request.GET.get('search_terms', '').strip()
        
        # make the query
        # get the field=value query from the selected facet options
        field_queries = u''
        for field in self.fields:
            value = request.GET.get(field['key'], '').strip()
            if value:
                if field['type'] == 'date':
                    from digipal.utils import get_range_from_date
                    rng = get_range_from_date(value)
                    field_queries += u' %s_min:<=%s %s_max:>=%s ' % (field['key'], rng[1], field['key'], rng[0])
                    #field_queries += u' %s_max:<=%s ' % (field['key'], rng[1])
                else:                    
                    field_queries += u' %s:"%s" ' % (field['key'], value)
        
        # add the search phrase    
        if search_phrase or field_queries:
            qp = self.get_whoosh_parser(index)
            q = qp.parse(u'%s %s' % (search_phrase, field_queries))
        else:
            from whoosh.query.qcore import Every
            q = Every()
            
        print q
            
        with index.searcher() as s:
            # run the query
            facets = self.get_whoosh_facets()

            #
            # result returned by search_page() doesn't support faceting
            # "'ResultsPage' object has no attribute 'groups'"
            # 
            # Two possible work-arounds:
            # 1. run two Whoosh searches (one for the groups/facets another for the specific page)
            # 2. run full faceted Whoosh search then paginate the ids
            #
            # TODO: check which one is the most efficient            
            # 
            #ret = s.search_page(q, 1, pagelen=10, groupedby=facets)
            
            sortedby = self.get_whoosh_sortedby(request)
            
            # Will only take top 10/25 results by default
            #ret = s.search(q, groupedby=facets)
            
            hand_filters.chrono('whoosh:')
            
            hand_filters.chrono('whoosh.search:')

            #ret = s.search(q, groupedby=facets, sortedby=sortedby, limit=1000000)
            ret = s.search(q, groupedby=facets, sortedby=sortedby, limit=1000000)
            #ret = s.search(q, groupedby=facets, limit=1000000)
            #ret = s.search(q, sortedby=sortedby, limit=1000000)
            #ret = s.search(q, limit=1000000)
            print facets
            #ret = s.search_page(q, 1, pagelen=10, groupedby=facets, sortedby=sortedby)
            
            hand_filters.chrono(':whoosh.search')

            hand_filters.chrono('whoosh.facets:')
            self.whoosh_groups = {}
            for field in self.fields:
                if field.get('count', False):
                    #self.whoosh_groups[field['key']] = ret.groups(field['key'])
                    self.whoosh_groups[field['key']] = {}
            hand_filters.chrono(':whoosh.facets')
        
            # convert the result into a list of model instances
            from django.core.paginator import Paginator
            
            hand_filters.chrono('whoosh.paginate:')
            # paginate
            self.ids = ret
            self.paginator = Paginator(ret, self.get_page_size(request))
            current_page = utils.get_int(request.GET.get('page'), 1)
            if current_page < 1: current_page = 1
            if current_page > self.paginator.num_pages:
                current_page = self.paginator.num_pages 
            self.current_page = self.paginator.page(current_page)
            ids = [hit['id'] for hit in self.current_page.object_list]
            hand_filters.chrono(':whoosh.paginate')
            
            print ids

            hand_filters.chrono(':whoosh')
            
            #print len(ids)
            
            #ids = [res['id'] for res in ret]
            
            hand_filters.chrono('sql:')
            
            records = self.get_all_records(True)
            records = records.in_bulk(ids)
            
            if len(records) != len(ids):
                raise Exception("DB query didn't retrieve all Whoosh results.")
            
            # 'item_part__historical_items'
            ret = [records[int(id)] for id in ids]

            hand_filters.chrono(':sql')

            # TODO: make sure the order is preserved
            
            
            # get facets
                    
        return ret
    
    def get_total_count(self):
        '''returns the total number of records in the result set'''
        return len(self.ids)
    
    def get_paginator(self):
        return getattr(self, 'paginator', Paginator([], 10))
    
    def get_current_page(self):
        ret = self.current_page
        return ret

    def get_whoosh_parser(self, index):
        from whoosh.qparser import MultifieldParser, GtLtPlugin
        
        # TODO: only active columns
        term_fields = [field['key'] for field in self.fields if field.get('search', False)]
        parser = MultifieldParser(term_fields, index.schema)
        parser.add_plugin(GtLtPlugin)
        return parser
    
    def get_selected_view(self):
        ret = self.views[0]
        for view in self.views:
            if view.get('selected', False):
                ret = view
                break
        return ret
    
    def get_page_size(self, request):
        ret = utils.get_int(request.GET.get('pgs'), 10)
        sizes = self.get_page_sizes()
        if ret not in sizes:
            ret = sizes[0]
        return ret     
    
    def get_page_sizes(self):
        ret = [10, 20, 50, 100]
        selected_view = self.get_selected_view()
        view_type = selected_view.get('type', 'list')
        if view_type == 'grid':
            ret = [9, 18, 30, 90]
        return ret
        
def get_types():
    image_options = {'key': 'image', 
                'label': 'Image',
                'model': Image,
                'fields': [
                           # label = the label displayed on the screen
                           # label_col = the label in the column in the result table
                           # type = the type of the field

                           # path = a field name (can go through a related object or call a function)
                           
                           # count = True to show the number of hits for each possible value of the field (i.e. show facet options)
                           # filter = True to let the user filter by this field
                           # search = True if the field can be searched on (phrase query)
                           # viewable = True if the field can be displayed in the result set

                           # index = True iff (search or filter or count)
                           
                           # e.g. ann: viewable, full_size: count, repo_city: viewable+count+search
                           # id: special
                           # Most of the times viewable => searchable but not always (e.g. ann.)
                           
                           {'key': 'url', 'label': 'Address', 'label_col': ' ', 'path': 'get_absolute_url', 'type': 'url', 'viewable': True},
                           #{'key': 'scribe', 'label': 'Scribe', 'path': 'hands__scribes__count', 'faceted': True, 'index': True},
                           #{'key': 'annotation', 'label': 'Annotations', 'path': 'annotations__count01', 'faceted': True, 'index': True},
                           #
                           {'key': 'hi_date', 'label': 'MS Date', 'path': 'item_part.historical_item.date', 'type': 'date', 'filter': True, 'viewable': True, 'search': True, 'id': 'hi_date', 'min': 500, 'max': 1300},
                           {'key': 'full_size', 'label': 'Image', 'path': 'get_media_right_label', 'type': 'boolean', 'count': True, 'search': True},
                           {'key': 'hi_type', 'label': 'Type', 'path': 'item_part.historical_item.historical_item_type.name', 'type': 'code', 'viewable': True, 'count': True},
                           {'key': 'hi_format', 'label': 'Format', 'path': 'item_part.historical_item.historical_item_format.name', 'type': 'code', 'viewable': True, 'count': True},
                           {'key': 'repo_city', 'label': 'Repository City', 'path': 'item_part.current_item.repository.place.name', 'count': True, 'search': True, 'viewable': True, 'type': 'title'},
                           {'key': 'repo_place', 'label': 'Repository Place', 'path': 'item_part.current_item.repository.name', 'count': True, 'search': True, 'viewable': True, 'type': 'title'},
                           {'key': 'shelfmark', 'label': 'Shelfmark', 'path': 'item_part.current_item.shelfmark', 'search': True, 'viewable': True, 'type': 'code'},
                           {'key': 'locus', 'label': 'Locus', 'path': 'locus', 'search': True, 'viewable': True, 'type': 'code'},
                           {'key': 'annotations', 'label_col': 'Ann.', 'label': 'Annotations', 'path': 'annotation_set.all.count', 'type': 'int', 'viewable': True},
                           {'key': 'thumbnail', 'label_col': 'Thumb.', 'label': 'Thumbnail', 'path': '', 'type': 'image', 'viewable': True, 'max_size': 70},
                           ],
                'select_related': ['item_part__current_item__repository__place'],
                'prefetch_related': ['item_part__historical_items', 'item_part__historical_items__historical_item_format', 'item_part__historical_items__historical_item_type'],
                'filter_order': ['hi_date', 'full_size', 'hi_type', 'hi_format', 'repo_city', 'repo_place'],
                'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date', 'annotations', 'hi_format', 'hi_type', 'thumbnail'],
                #'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date'],
                'sorted_fields': ['repo_city', 'repo_place', 'shelfmark', 'locus'],
                'views': [
                          {'icon': 'th-list', 'label': 'List', 'key': 'list'},
                          {'icon': 'th', 'label': 'Grid', 'key': 'grid', 'type': 'grid'},
                          ],
                }
    
    graph_options = {'key': 'graph', 
                'label': 'Graph',
                'model': Graph,
                'django_filter': {'annotation__isnull': False},
                'fields': [
                           {'key': 'url', 'label': 'Address', 'label_col': ' ', 'path': 'get_absolute_url', 'type': 'url', 'viewable': True},
#                            {'key': 'hi_date', 'label': 'MS Date', 'path': 'item_part.historical_item.date', 'type': 'date', 'filter': True, 'viewable': True, 'search': True, 'id': 'hi_date', 'min': 500, 'max': 1300},
#                            {'key': 'full_size', 'label': 'Image', 'path': 'get_media_right_label', 'type': 'boolean', 'count': True, 'search': True},
#                            {'key': 'hi_type', 'label': 'Type', 'path': 'item_part.historical_item.historical_item_type.name', 'type': 'code', 'viewable': True, 'count': True},
#                            {'key': 'hi_format', 'label': 'Format', 'path': 'item_part.historical_item.historical_item_format.name', 'type': 'code', 'viewable': True, 'count': True},
                            {'key': 'repo_city', 'label': 'Repository City', 'path': 'annotation.image.item_part.current_item.repository.place.name', 'count': True, 'search': True, 'viewable': True, 'type': 'title'},
                            {'key': 'repo_place', 'label': 'Repository Place', 'path': 'annotation.image.item_part.current_item.repository.name', 'count': True, 'search': True, 'viewable': True, 'type': 'title'},
                            {'key': 'shelfmark', 'label': 'Shelfmark', 'path': 'annotation.image.item_part.current_item.shelfmark', 'search': True, 'viewable': True, 'type': 'code'},
                            {'key': 'locus', 'label': 'Locus', 'path': 'annotation.image.locus', 'search': True, 'viewable': True, 'type': 'code'},
#                            {'key': 'annotations', 'label_col': 'Ann.', 'label': 'Annotations', 'path': 'annotation_set.all.count', 'type': 'int', 'viewable': True},
#                            {'key': 'thumbnail', 'label_col': 'Thumb.', 'label': 'Thumbnail', 'path': '', 'type': 'image', 'viewable': True, 'max_size': 70},
#                            {'key': 'script', 'label': 'Script', 'path': 'idiograph.allograh.script.name', 'viewable': True, 'type': 'code'},
                            {'key': 'chartype', 'label': 'Character Type', 'path': 'idiograph.allograph.character.ontograph.ontograph_type.name', 'viewable': True, 'type': 'code', 'count': True},
                            {'key': 'character', 'label': 'Character', 'path': 'idiograph.allograph.character.name', 'viewable': True, 'type': 'code', 'count': True},
                            {'key': 'allograph', 'label': 'Allograph', 'path': 'idiograph.allograph.name', 'viewable': True, 'type': 'code', 'count': True},
                           ],
                'select_related': ['annotation__item_part__current_item__repository__place', 
                                   'idiograph__allograph__character__ontograph__ontograph_type', 
                                   ],
                'prefetch_related': ['annotation__image__item_part__historical_items', 'annotation__image__item_part__historical_items__historical_item_format', 'annotation__image__item_part__historical_items__historical_item_type'],
                'filter_order': ['repo_city', 'repo_place'],
                #'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date', 'annotations', 'hi_format', 'hi_type', 'thumbnail'],
                #'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date'],
                'sorted_fields': ['repo_city', 'repo_place', 'shelfmark', 'locus'],
                'views': [
                          {'icon': 'th-list', 'label': 'List', 'key': 'list'},
                          {'icon': 'th', 'label': 'Grid', 'key': 'grid', 'type': 'grid'},
                          ],
                }
    #ret = [FacetedModel(image_options)]
    ret = [FacetedModel(graph_options)]
    return ret

def search_whoosh_view(request, content_type='', objectid='', tabid=''):
    hand_filters.chrono('VIEW:')
    
    hand_filters.chrono('SEARCH:')

    context = {'tabid': tabid}
    
    # select the content type 
    cts = get_types()
    ct_key = request.REQUEST.get('result_type', cts[0].key)
    for ct in cts:
        if ct.key == ct_key:
            break

    context['result_type'] = ct
    
    # run the search
    records = ct.get_requested_records(request)
    
    # add the search parameters to the template
    context['facets'] = ct.get_facets(request)
    
    context['cols'] = ct.get_columns()
    
    # add the results to the template 
    context['result'] = list(records)
    
    context['current_page'] = ct.get_current_page()

    context['summary'] = ct.get_summary(request)
    
    context['advanced_search_form'] = True
    
    context['page_sizes'] = ct.get_page_sizes()
    context['page_size'] = ct.get_page_size(request)
    context['hit_count'] = ct.get_total_count()
    context['views'] = ct.views
    
    hand_filters.chrono(':SEARCH')

    hand_filters.chrono('TEMPLATE:')
    
    ret = render_to_response('search/faceted/search_whoosh.html', context, context_instance=RequestContext(request))

    hand_filters.chrono(':TEMPLATE')

    hand_filters.chrono(':VIEW')
    
    return ret

def rebuild_index():
    for ct in get_types():
        index = create_index_schema(ct)
        if index:
            populate_index(ct, index)

def create_index_schema(ct):
    print '%s' % ct.key
    
    print '\tcreate schema'
    
    # create schema
    from whoosh.fields import TEXT, ID, NGRAM, NUMERIC, KEYWORD
    fields = {'id': ID(stored=True)}
    for field in ct.fields:
        if ct.is_field_indexable(field):
            for suffix, whoosh_type in get_whoosh_field_types(field).iteritems():
                fields[field['key']+suffix] = whoosh_type
        
    print '\t' + ', '.join(key for key in fields.keys())
    
    print '\trecreate empty index'

    # recreate an empty index
    import os
    from whoosh.fields import Schema
    from digipal.utils import recreate_whoosh_index
    ret = recreate_whoosh_index(os.path.join(settings.SEARCH_INDEX_PATH, 'faceted'), ct.key, Schema(**fields))
    return ret        

def get_whoosh_field_types(field):
    ret = {}
    
    if field['type'] == 'date':
        ret[''] = get_whoosh_field_type({'type': 'code'})
        ret['_min'] = get_whoosh_field_type({'type': 'int'})
        ret['_max'] = get_whoosh_field_type({'type': 'int'})
    else:
        ret[''] = get_whoosh_field_type(field)
    
    whoosh_sortable_field = FacetedModel._get_sortable_whoosh_field(field)
    if whoosh_sortable_field and whoosh_sortable_field != field['key']:
        ret['_sortable'] = get_whoosh_field_type({'type': 'int'})
    
    return ret

def get_whoosh_field_type(field):
    '''
    Defines Whoosh field types used to define the schemas.
    See get_field_infos().
    '''
    
    # see http://pythonhosted.org/Whoosh/api/analysis.html#analyzers
    # see JIRA 165
    
    from whoosh.fields import TEXT, ID, NUMERIC
    # TODO: shall we use stop words? e.g. 'A and B' won't work? 
    from whoosh.analysis import SimpleAnalyzer, StandardAnalyzer, StemmingAnalyzer, CharsetFilter
    from whoosh.support.charset import accent_map
    # ID: as is; SimpleAnalyzer: break into lowercase terms, ignores punctuations; StandardAnalyzer: + stop words + minsize=2; StemmingAnalyzer: + stemming
    # minsize=1 because we want to search for 'Scribe 2'
    
    # A paragraph or more.
    field_type = field['type']
    if field_type == 'id':
        # An ID (e.g. 708-AB)
        ret = ID(stored=True, sortable=True)
    elif field_type in ['int']:
        ret = NUMERIC(sortable=True)
    elif field_type in ['code']:
        # A code (e.g. K. 402, Royal 7.C.xii)
        # See JIRA 358
        ret = TEXT(analyzer=SimpleAnalyzer(ur'[.\s()\u2013\u2014-]', True), stored=True, sortable=True)
    elif field_type == 'title':
        # A title (e.g. British Library)
        ret = TEXT(analyzer=StemmingAnalyzer(minsize=1, stoplist=None) | CharsetFilter(accent_map), stored=True, sortable=True)
    elif field_type == 'short_text':
        # A few words.
        ret = TEXT(analyzer=StemmingAnalyzer(minsize=1) | CharsetFilter(accent_map), stored=True, sortable=True)
    else:
        ret = TEXT(analyzer=StemmingAnalyzer(minsize=1) | CharsetFilter(accent_map), stored=True, sortable=True)
        
    return ret
    
def populate_index(ct, index):
    # Add documents to the index
    print '\tgenerate sort rankings'
    ct.prepare_value_rankings()
    
    print '\tretrieve all records'
    writer = index.writer()
    rcs = ct.get_all_records(True)
    
    print '\tadd records to index'
    for record in rcs:
        writer.add_document(**ct.get_document_from_record(record))
    
    writer.commit()
    print '\tdone (%s records)' % rcs.count()
    