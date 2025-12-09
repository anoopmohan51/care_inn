from django.db.models import Model
from .mixins.filter_parser import FilterParserMixin
from .mixins.query_builder import QueryBuilderMixin
from .mixins.field_handler import FieldHandlerMixin
from .mixins.pagination import PaginationMixin

class GlobalFilter(
    FilterParserMixin, 
    QueryBuilderMixin, 
    FieldHandlerMixin, 
    PaginationMixin
):
    def __init__(
        self,
        request,
        field_lookup:dict,
        model:Model,
        exclude:list
    ):
        self.request = request
        self.field_lookup = field_lookup
        self.model = model
        self.exclude = exclude
        self.filter_by=request.data.get('filters') or []
        self.sort_by=request.data.get('sort_by') or []
    
    def get_count(self,queryset):
        return queryset.count()
        
    def _get_result(self,*args,**kwargs):
        fields = self.get_fields_for_result(args,kwargs)
        print("#########################",fields)
        filter_args, sort_args = self.get_query()
        print("#########################",filter_args)
        print("#########################",sort_args)

        queryset = self.model.objects.annotate(*args, **kwargs).filter(filter_args).values(*fields).distinct()
        count = self.get_count(queryset)
        if sort_args:
            queryset = queryset.order_by(*sort_args)
        return queryset, count 
    
    