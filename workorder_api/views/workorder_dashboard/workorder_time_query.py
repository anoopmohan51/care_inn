from django.db import connection
from .workorder_type_count import dictfetchall

def get_workorder_time_query(tenant_id,start_date,end_date):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT
                    AVG(
                        COALESCE(
                            EXTRACT(EPOCH FROM (begin_activity.first_begin - w.created_at)),
                            0
                        )
                    ) AS avg_initial_response_time_seconds,

                    AVG(
                        COALESCE(
                            EXTRACT(EPOCH FROM (
                                COALESCE(close_activity.closed_at, w.end_date) - w.created_at
                            )),
                            0
                        )
                    ) AS avg_resolution_time_seconds

                FROM workorder w

                LEFT JOIN (
                    SELECT
                        workorder_id,
                        MIN(created_at) AS first_begin
                    FROM workorder_activity
                    WHERE activity = 'TIMER_START'
                    GROUP BY workorder_id
                ) begin_activity
                    ON begin_activity.workorder_id = w.id

                LEFT JOIN (
                    SELECT DISTINCT ON (workorder_id)
                        workorder_id,
                        created_at AS closed_at
                    FROM workorder_activity
                    WHERE activity = 'CLOSED'
                    ORDER BY workorder_id, created_at DESC
                ) close_activity
                    ON close_activity.workorder_id = w.id

                WHERE w.tenant_id = %(tenant_id)s
                AND w.created_at::date BETWEEN %(start_date)s AND %(end_date)s
                AND w.is_delete = FALSE;
                """,{ "tenant_id":tenant_id, "start_date":start_date, "end_date":end_date}
        )
        return dictfetchall(cursor)