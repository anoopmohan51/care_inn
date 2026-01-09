from django.db import connection
from workorder_api.views.workorder_dashboard.workorder_count_per_day import dictfetchall

def _get_workorder_summary(tenant_id,workorder_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT 
                    w.created_at AS created_date,

                    COALESCE(close_activity.closed_at, w.end_date) AS closed_date,

                    EXTRACT(EPOCH FROM (begin_activity.first_begin - w.created_at)) / 3600 
                        AS initial_response_time_hours,

                    EXTRACT(EPOCH FROM (
                        COALESCE(close_activity.closed_at, w.end_date) - w.created_at
                    )) / 3600 AS resolution_time_hours,

                    COALESCE(timeline_sum.total_duration, 0) AS total_working_time_minutes,
                    COALESCE(timeline_sum.total_duration / 60.0, 0) AS total_working_time_hours

                FROM workorder w

                LEFT JOIN (
                    SELECT 
                        workorder_id,
                        MIN(created_at) AS first_begin
                    FROM workorder_activity
                    WHERE activity = 'BEGIN'
                    GROUP BY workorder_id
                ) begin_activity 
                    ON begin_activity.workorder_id = w.id

                LEFT JOIN (
                    SELECT 
                        workorder_id,
                        MAX(created_at) AS closed_at
                    FROM workorder_activity
                    WHERE activity = 'STATUS'
                    AND to_value = 'CLOSED'
                    GROUP BY workorder_id
                ) close_activity 
                    ON close_activity.workorder_id = w.id

                LEFT JOIN (
                    SELECT 
                        workorder_id,
                        SUM(duration) AS total_duration
                    FROM workorder_timeline
                    WHERE is_delete = FALSE
                    GROUP BY workorder_id
                ) timeline_sum 
                    ON timeline_sum.workorder_id = w.id

                WHERE w.id = %s
                AND w.tenant_id = %s
                AND w.is_delete = FALSE""",
            [tenant_id,workorder_id]
        )
        return dictfetchall(cursor)