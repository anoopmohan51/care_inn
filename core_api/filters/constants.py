# filters/constants.py
FILTER_CONDITION_LOOKUP = {
    "is": "iexact",
    "startswith": "istartswith",
    "contains": "icontains",
    "like": "icontains",
    "greater than": "gt",
    "less than": "lt",
    "is not": "iexact",
    "less than or equal": "lte",
    "greater than or equal": "gte",
    "ends with": "iendswith",
    "equalto": "exact",
    "datelessthanequal": "date__lte",
    "dategreaterthanequal": "date__gte",
    "date_between": "range",
    "exactdate": "date",
    "dategreaterthan": "date__gt",
    "datelessthan": "date__lt",
    "is_null": "isnull",
    "in": "in",
    "key": "has_keys",
    "not_equalto": None,
    "regex": "iregex"
}

FILTER_CONDITION_OPERATORS = {
    "is": "=",
    "greater than": ">",
    "less than": "<",
    "is not": "!=",
    "less than or equal": "<=",
    "greater than or equal": ">=",
    "equalto": "=",
    "datelessthanequal": "<=",
    "dategreaterthanequal": ">=",
    "exactdate": "=",
    "dategreaterthan": ">",
    "datelessthan": "<",
    "is_null": "IS NULL"
}
