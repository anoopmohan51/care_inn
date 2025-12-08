from django.db.models import Q

OPERATORS = {
    "is": "iexact",
    "contains": "icontains",
    "startswith": "istartswith",
    "endswith": "iendswith",
    "greater_than": "gt",
    "less_than": "lt",
    "gte": "gte",
    "lte": "lte",
    "in": "in",
    "is_null": "isnull",
    "not": None,     # negation
    "range": "range"
}

class PayloadConditionMixin:
    def create_q_object(self,condition):
        field_name = condition.get('field')
        operator = condition.get('operator')
        value = condition.get('value')
        lookup = OPERATORS.get(operator)
        if lookup is None:
            return ~Q(**{field_name: value})
        lookup_expression = f"{field_name}__{lookup}"
        return Q(**{lookup_expression: value})

class PayloadFilterMixin(PayloadConditionMixin):
    def build_paload_query(self):
        payload_filters = self.request.query_params.get('filters',None)

        main_query = Q()
        for block in payload_filters:
            if "conditions" in block:
                block_operator = block.get("operator","AND")
                nested_query = Q()
                for condition in block.get("conditions",[]):
                    q_object = self.create_q_object(condition)
                    if block_operator == "AND":
                        nested_query &= q_object
                    else:
                        nested_query |= q_object
                main_query &= nested_query
            else:
                q_object = self.create_q_object(block)
                main_query &= q_object
            
        return main_query

class 

class BaseFilter(PayloadFilterMixin):
    def __init__(self,request,model):
        self.request = request
        self.model = model

    def get_queryset(self):
        return self.model.objects.filter(self.build_paload_query())

    def get_serializer(self):
        return self.model.serializer