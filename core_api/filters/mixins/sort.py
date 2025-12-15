from django.db.models import F, CharField, TextField
from django.db.models.functions import Lower

class SortMixin:

    def build_sort_args(self):
        sort_args = []
        for rule in self.sort_by:
            column = self.field_lookup.get(rule["colname"])
            direction = rule["direction"]

            try:
                column_type = self.model._meta.get_field(column)
            except:
                column_type = None

            if isinstance(column_type, (CharField, TextField)):
                expr = Lower(column)
            else:
                expr = F(column)

            sort_args.append(expr.desc(nulls_last=True) if direction == "desc" else expr)

        return sort_args