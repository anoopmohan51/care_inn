from django.db import connection
from workorder_api.views.workorder_dashboard.workorder_count_per_day import dictfetchall

def _get_workorder_summary(tenant_id,workorder_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT
                    w.created_at AS created_date,

                    COALESCE(close_activity.closed_at, w.end_date) AS closed_date,

                    --Initial response time (hours)
                    EXTRACT(EPOCH FROM (begin_activity.first_begin - w.created_at)) / 3600
                        AS initial_response_time_hours,

                    -- Resolution time (hours)
                    EXTRACT(EPOCH FROM (
                        COALESCE(close_activity.closed_at, w.end_date) - w.created_at
                    )) / 3600 AS resolution_time_hours,

                    --Total working time (minutes)
                    COALESCE(timeline_sum.total_duration, 0) AS total_working_time_minutes,

                    --Created user name
                    CONCAT(cu.first_name, ' ', cu.last_name) AS created_user_name,

                    --Closed user name
                    CONCAT(clu.first_name, ' ', clu.last_name) AS closed_user_name

                    FROM workorder w

                    -- Created user
                    LEFT JOIN core_api_appusers cu
                        ON cu.id = w.created_user_id

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
                            created_at AS closed_at,
                            initiated_by_id
                        FROM workorder_activity
                        WHERE activity = 'STATUS'
                        AND to_value = 'CLOSED'
                        ORDER BY workorder_id, created_at DESC
                    ) close_activity
                        ON close_activity.workorder_id = w.id

                    -- Closed user
                    LEFT JOIN core_api_appusers clu
                        ON clu.id = close_activity.initiated_by_id

                    -- Timeline total duration
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
                    AND w.is_delete = FALSE
                """,[workorder_id,tenant_id]
        )
        return dictfetchall(cursor)