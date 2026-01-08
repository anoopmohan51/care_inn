from django.db import connection
from .workorder_type_count import dictfetchall

def get_workorder_count_per_day(tenant_id,days):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            WITH days AS (
                SELECT
                    d::date AS date
                FROM generate_series(
                    CURRENT_DATE -  ((%s - 1) * INTERVAL '1 day'),
                    CURRENT_DATE,
                    INTERVAL '1 day'
                ) AS d
            )
            SELECT
                days.date,
                COALESCE(COUNT(w.id), 0) AS count
            FROM days
            LEFT JOIN workorder w
                ON DATE(w.created_at) = days.date
                AND w.is_delete = FALSE
                AND w.tenant_id = %s
            GROUP BY days.date
            ORDER BY days.date
        """, [days,tenant_id]
        )
        return dictfetchall(cursor)