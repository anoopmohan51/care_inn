from django.db import connection
from workorder_api.views.workorder_dashboard.workorder_count_per_day import dictfetchall

def _get_users(user_group_id,limit,offset):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT 
                au.id,
                au.first_name,
                au.last_name,
                au.email,
                au.phone,
                au.status,
                au.designation,
                au.created_at,
                au.updated_at,
                r.name AS role_name,
                p.name AS position_name,
                t.name AS tenant_name,

                CASE 
                    WHEN ugu.user_id IS NOT NULL THEN TRUE
                    ELSE FALSE
                END AS is_member

            FROM core_api_appusers au

            LEFT JOIN user_group_users ugu
                ON au.id = ugu.user_id
            AND ugu.user_group_id = %s

            LEFT JOIN core_api_role r 
                ON au.role_id = r.id

            LEFT JOIN core_api_position p 
                ON au.position_id = p.id

            LEFT JOIN tenant t 
                ON au.tenant_id = t.id

            WHERE au.is_delete = FALSE

            ORDER BY 
                is_member DESC,
                au.created_at DESC

            LIMIT %s OFFSET %s""",
            [user_group_id,limit,offset]
        )
        return dictfetchall(cursor)