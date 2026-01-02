from django.db import connection

def get_workorder_type_count(tenant_id,start_date,end_date):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                    COUNT(*) FILTER (WHERE workorder_type='COMPLAINT') AS total_complaints,
                    COUNT(*) FILTER (WHERE workorder_type='REQUEST') AS total_requests,
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


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]