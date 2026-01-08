from django.db.models import F,Value
from django.db.models.functions import Concat
from django.db.models.fields.related import ManyToOneRel, OneToOneRel

class FieldHandlerMixin:

    def get_model_fields(self,model):
        fields = []
        for f in model._meta.get_fields():
            if not isinstance(f, (ManyToOneRel, OneToOneRel)):
                if hasattr(f, 'column') or hasattr(f, 'attname'):
                    fields.append(f.name)

        for column in getattr(self, "exclude", []) or []:
            if column in fields:
                fields.remove(column)
        return fields
    
    def get_fields_for_result(self,args:tuple,kwargs:dict):
        fields = set(self.get_model_fields(self.model))
        annotated_fields = set(kwargs.keys())
        fields.update(annotated_fields)
        return fields