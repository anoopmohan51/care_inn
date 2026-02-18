from django.db import connection
from .workorder_type_count import dictfetchall

def get_workorder_time_query(tenant_id,start_date,end_date):
    with connection.cursor() as cursor:
        cursor.execute(
            """WITH workorder_times AS (
                    SELECT
                        -- Initial response time (seconds)
                        EXTRACT(EPOCH FROM (begin_activity.first_begin - w.created_at)) 
                            AS initial_response_time,

                        -- Resolution time (seconds)
                        EXTRACT(EPOCH FROM (
                            COALESCE(close_activity.closed_at, w.end_date) - w.created_at
                        )) 
                            AS resolution_time

                    FROM workorder w

                    -- First BEGIN activity
                    LEFT JOIN (
                        SELECT
                            workorder_id,
                            MIN(created_at) AS first_begin
                        FROM workorder_activity
                        WHERE activity = 'TIMER_START'
                        GROUP BY workorder_id
                    ) begin_activity
                        ON begin_activity.workorder_id = w.id

                    -- Latest CLOSED status
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
                    AND w.is_delete = FALSE
                    AND w.created_at::date BETWEEN %(start_date)s AND %(end_date)s
                )

                SELECT
                    -- Average Initial Response Time (seconds)
                    COALESCE(AVG(initial_response_time), 0) 
                        AS average_initial_response_time_seconds,

                    -- Average Resolution Time (seconds)
                    COALESCE(AVG(resolution_time), 0) 
                        AS average_resolution_time_seconds

                FROM workorder_times;
                """,{ "tenant_id":tenant_id, "start_date":start_date, "end_date":end_date}
        )
        return dictfetchall(cursor)