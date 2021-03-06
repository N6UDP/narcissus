import logging
log = logging.getLogger('narcissus')

from moksha.connector import IConnector, ICall, IQuery, ParamFilter, ISearch

class NarcissusConnector(IConnector, ICall, ISearch, IQuery):
    _method_paths = {}
    _query_paths = {}

    # ICall
    def call(self, resource_path, params=None, *args):
        return 'NarcissusConnector.call(%r)' % resource_path

    # IQuery
    @classmethod
    def register(cls):
        cls.register_query_stuff()
        cls.register_search_stuff()

    @classmethod
    def register_query_stuff(cls):
        path = cls.register_query('query_stuff',
                                  cls.query_stuff,
                                  primary_key_col='id',
                                  default_sort_col='id',
                                  default_sort_order=-1,
                                  can_paginate=True)
        path.register_column('id',
                             default_visible=True,
                             can_sort=True,
                             can_filter_wildcards=False)
        path.register_column('name',
                             default_visible=True,
                             can_sort=True,
                             can_filter_wildcards=True)
        f = ParamFilter()
        f.add_filter('argument', allow_none=True)
        cls._query_stuff_filter = f

    def query_stuff(self, start_row=None, rows_per_page=None, order=-1, sort_col=None,
                    filters=None, **params):
        if not filters:
            filters = {}

        # Replace this with something useful
        total_count = 2
        rows = [{'id': 0, 'name': 'foo'}, {'id': 1, 'name': 'bar'}]
        if filters.get('argument'):
            rows.append({'id': 2, 'name': filters['argument']})
        if order < 0:
            rows.reverse()

        return (total_count, rows)

    # ISearch
    @classmethod
    def register_search_stuff(cls):
        path = cls.register_search_path('search_stuff',
                                        cls.search_stuff,
                                        primary_key_col='name',
                                        default_sort_col='name',
                                        default_sort_order=-1,
                                        can_paginate=True)
        path.register_column('id',
                             default_visible=True,
                             can_sort=True,
                             can_filter_wildcards=False)
        path.register_column('name',
                             default_visible=True,
                             can_sort=True,
                             can_filter_wildcards=True)

    def search_stuff(self, search_term):
        return [{'id': 0, 'name': search_term}]
