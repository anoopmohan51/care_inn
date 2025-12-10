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
        base_filter =None,
        default_sort:str = None,
        exclude:list = None
    ):
        self.request = request
        self.field_lookup = field_lookup
        self.model = model
        self.exclude = exclude
        self.filter_by=request.data.get('filters') or []
        self.sort_by=request.data.get('sort_by') or []
        self.base_filter = base_filter
        self.default_sort = default_sort

        
    
    def get_count(self,queryset):
        return queryset.count()
        
    def _get_result(self,*args,**kwargs):
        fields = self.get_fields_for_result(args,kwargs)
        filter_args, sort_args = self.get_query()
        queryset = self.model.objects.annotate(*args, **kwargs).filter(filter_args).values(*fields).distinct()
        count = self.get_count(queryset)
        if sort_args:
            queryset = queryset.order_by(*sort_args)
        return queryset, count
    
    def get_serialized_result(self,*args,**kwargs):
        filter_args, sort_args = self.get_query()
        limit = self._get_limit()
        offset = self._get_offset()
        queryset = self.model.objects.filter(filter_args).distinct()
        count = self.get_count(queryset)
        if sort_args:
            queryset = queryset.order_by(*sort_args)
        serializer_instance = serializer(queryset[offset:offset+limit], many=True)
        return serializer_instance.data, count