from django.db import connection
from .workorder_type_count import dictfetchall

def get_workorder_time_query(tenant_id,start_date,end_date):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT
    COALESCE(
        EXTRACT(EPOCH FROM AVG(first_response_time)) / 3600,
        INTERVAL '0'
    ) AS avg_initial_response_time,

    COALESCE(
        AVG(resolution_time_minutes),
        0
    ) AS avg_resolution_time_minutes
FROM (
    SELECT
        w.id AS workorder_id,

        MIN(
            CASE 
                WHEN wa.activity = 'BEGIN' 
                THEN wa.created_at 
            END
        ) - w.created_at AS first_response_time,

        EXTRACT(EPOCH FROM (
            MAX(
                CASE 
                    WHEN wa.activity = 'TIME_END' 
                    THEN wa.created_at 
                END
            )
            -
            MIN(
                CASE 
                    WHEN wa.activity = 'TIME_START' 
                    THEN wa.created_at 
                END
            )
        )) / 60 AS resolution_time_minutes

    FROM workorder w
    LEFT JOIN workorder_activity wa
        ON wa.workorder_id = w.id
    WHERE
        w.is_delete = FALSE
        AND w.tenant_id = %s
        AND w.created_at::date BETWEEN %s AND %s
    GROUP BY
        w.id, w.created_at
) t
WHERE
    first_response_time IS NOT NULL
    AND resolution_time_minutes IS NOT NULL;""", [tenant_id, start_date, end_date]
        )
        return dictfetchall(cursor)