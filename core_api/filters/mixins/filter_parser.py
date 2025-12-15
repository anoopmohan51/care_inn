from django.db.models import Q
from core_api.filters.constants import FILTER_CONDITION_LOOKUP


class FilterParserMixin:

    def parse_condition(self,condition:dict):
        column = self.field_lookup.get(condition['colname'])
        lookup = FILTER_CONDITION_LOOKUP.get(condition['condition'])
        key = column if lookup is None else f"{column}__{lookup}"
        return key, condition.get('value'),lookup
    
    def built_condition_query(self,condition:dict):
        key, value, lookup = self.parse_condition(condition)
        if lookup=="isnull":
            return Q(**{key:bool(value)})
        if lookup is None:
            return ~Q(**{key:value})
        return Q(**{key:value})
