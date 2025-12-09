from django.db.models import F,Value
from django.db.models.functions import Concat

class FieldHandlerMixin:

    def get_model_fields(self,model):
        fields = [f.name for f in model._meta.get_fields()]
        for column in getattr(self, "exclude", []) or []:
            if column in fields:
                fields.remove(column)
        return fields
    
    def get_fields_for_result(self,args:tuple,kwargs:dict):
        fields = set(self.get_model_fields(self.model))
        annotated_fields = set(kwargs.keys())
        fields.update(annotated_fields)
        return fields