from django.db import connection
from .workorder_type_count import dictfetchall

def get_workorder_count_per_day(tenant_id,start_date,end_date):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                DATE(created_at) AS date,
                COUNT(*) AS count
            FROM
                workorder
            WHERE
                is_delete = FALSE AND
                tenant_id = %s AND 
                created_at BETWEEN %s AND %s
            GROUP BY
                DATE(created_at)
        """, [tenant_id, start_date, end_date]
        )
        return dictfetchall(cursor)