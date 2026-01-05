from django.db import connection

def get_workorder_type_count(tenant_id,start_date,end_date):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT
                    COUNT(*) FILTER (WHERE s.service_type='COMPLAINT') AS total_complaints,
                    COUNT(*) FILTER (WHERE s.service_type='REQUEST') AS total_requests,
                    COUNT(*) FILTER (WHERE workorder_type='MAINTENANCE') AS total_maintenance,
                    COUNT(*) AS total_workorders
            FROM
                workorder w
            JOIN workorder_api_services s ON w.service_id = s.id

            WHERE
                w.is_delete = FALSE AND
                w.tenant_id = %s AND 
                w.created_at :: date BETWEEN %s AND %s
        """, [tenant_id, start_date, end_date]
        )
        return dictfetchall(cursor)


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]