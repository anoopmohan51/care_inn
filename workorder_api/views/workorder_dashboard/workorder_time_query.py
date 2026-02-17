from django.db import connection
from .workorder_type_count import dictfetchall

def get_workorder_time_query(tenant_id,start_date,end_date):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT
                    COALESCE(AVG(t.first_response_seconds) / 3600, 0) 
                        AS avg_initial_response_time_hours,

                    COALESCE(AVG(t.resolution_time_minutes), 0) 
                        AS avg_resolution_time_minutes

                FROM (
                    SELECT
                        w.id AS workorder_id,

                        /* First Response Time (convert to seconds immediately) */
                        EXTRACT(EPOCH FROM (
                            MIN(
                                CASE
                                    WHEN wa.activity = 'BEGIN'
                                    THEN wa.created_at
                                END
                            ) - w.created_at
                        )) AS first_response_seconds,

                        /* Resolution Time (in minutes) */
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
                        AND w.tenant_id = %(tenant_id)s
                        AND w.created_at::date BETWEEN %(start_date)s AND %(end_date)s

                    GROUP BY
                        w.id, w.created_at

                ) t

                WHERE
                    t.first_response_seconds IS NOT NULL
                    AND t.resolution_time_minutes IS NOT NULL;
                """,{ "tenant_id":tenant_id, "start_date":start_date, "end_date":end_date}
        )
        return dictfetchall(cursor)