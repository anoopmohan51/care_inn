from django.db.models import Q

class QueryBuilderMixin:
    def build_group_query(self,group :dict):
        query = Q()
        next_operator = None
        for condition in group.get('conditions',[]):
            query_object = self.built_condition_query(condition)
            if next_operator=="OR":
                query |= query_object
            else:
                query &= query_object
            next_operator = group.get('operator')
        return query
    
    def build_main_filter_query(self,filters:list):
        main_query = Q()
        for filter in filters:
            group_query = self.build_group_query(filter)
            if filter.get('operator')=="AND":
                main_query &= group_query
            else:
                main_query |= group_query
        return main_query
    
    def get_query(self):
        filter_query = Q(is_delete=False)
        sort_query = []
        if self.filter_by:
            filter_query = self.build_main_filter_query(self.filter_by)
        return filter_query, sort_query
        # if self.sort_by:
            
        
