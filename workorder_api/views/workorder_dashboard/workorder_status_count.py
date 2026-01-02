from django.db import connection
from .workorder_type_count import dictfetchall

def get_workorder_status_count(tenant_id,start_date,end_date):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                COUNT(*) FILTER (WHERE status='UNASSIGNED') AS total_unassigned,
                COUNT(*) FILTER (WHERE status='ASSIGNED NOT STARTED') AS total_assigned_not_started,
                COUNT(*) FILTER (WHERE status='IN PROGRESS') AS total_in_progress,
                COUNT(*) FILTER (WHERE status='PAUSED') AS total_paused,
                COUNT(*) FILTER (WHERE status='CLOSED') AS total_closed,
                COUNT(*) AS total_workorders
            FROM
                workorder
            WHERE
                is_delete = FALSE AND
                tenant_id = %s AND 
                created_at BETWEEN %s AND %s
        """, [tenant_id, start_date, end_date]
        )
        return dictfetchall(cursor)