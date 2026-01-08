from django.db import connection
from .workorder_type_count import dictfetchall

def get_workorder_type_count_perweekdays(tenant_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT
                    TO_CHAR(created_at, 'Dy') AS day,
                    EXTRACT(DOW FROM created_at) AS day_order,
                    COUNT(*) FILTER (WHERE workorder_type = 'REQUEST') AS request,
                    COUNT(*) FILTER (WHERE workorder_type = 'COMPLAINT') AS complaint
                FROM workorder
                WHERE is_delete = FALSE AND
                tenant_id = %s AND
                created_at >= CURRENT_DATE - INTERVAL '6 days'
                GROUP BY day, day_order
                ORDER BY day_order""", [tenant_id]
        )
        return dictfetchall(cursor)