from django.db import connection
from .workorder_type_count import dictfetchall

def get_workorder_type_count_perweekdays(tenant_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """WITH days AS (
                        SELECT
                            d::date AS day_date,
                            TO_CHAR(d, 'Dy') AS day,
                            EXTRACT(DOW FROM d) AS day_order
                        FROM generate_series(
                            CURRENT_DATE - INTERVAL '6 days',
                            CURRENT_DATE,
                            INTERVAL '1 day'
                        ) AS d
                    )
                SELECT
                    days.day,
                    days.day_order,
                    COALESCE(
                        COUNT(w.*) FILTER (WHERE w.workorder_type = 'REQUEST'),
                        0
                    ) AS request,
                    COALESCE(
                        COUNT(w.*) FILTER (WHERE w.workorder_type = 'COMPLAINT'),
                        0
                    ) AS complaint
                FROM days
                LEFT JOIN workorder w
                    ON w.created_at::date = days.day_date
                    AND w.is_delete = FALSE
                    AND w.tenant_id = %s
                GROUP BY days.day, days.day_order, days.day_date
                ORDER BY days.day_order;
                """, [tenant_id]
        )
        return dictfetchall(cursor)