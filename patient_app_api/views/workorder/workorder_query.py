from django.db import connection
from workorder_api.views.workorder_dashboard.workorder_count_per_day import dictfetchall

def get_workorder_query(tenant_id,mrd_id,limit,offset):
    with connection.cursor() as cursor:
        cursor.execute(
            """
           SELECT *
            FROM (
                /* ---------- workorder_temp ---------- */
                SELECT
                    id,
                    workorder_type,
                    assignee_type,
                    description,
                    priority,
                    when_to_start,
                    sla_minutes,
                    mrd_id,
                    status,
                    created_at,
                    updated_at,
                    is_delete,
                    unique_id,
                    source,
                    start_date,
                    end_date,
                    is_approved,
                    room_id        AS room,
                    user_id        AS "user",
                    user_group_id  AS user_group,
                    tenant_id      AS tenant,
                    created_user_id AS created_user,
                    updated_user_id AS updated_user,
                    service_id     AS service
                FROM workorder_temp
                WHERE tenant_id = %(tenant_id)s
                AND mrd_id = %(mrd_id)s
                AND mrd_id = '123'
                AND is_delete = FALSE
                AND is_approved = FALSE

                UNION ALL

                /* ---------- workorder ---------- */
                SELECT
                    id,
                    workorder_type,
                    assignee_type,
                    description,
                    priority,
                    when_to_start,
                    sla_minutes,
                    mrd_id,
                    status,
                    created_at,
                    updated_at,
                    is_delete,
                    unique_id,
                    source,
                    start_date,
                    end_date,
                    TRUE            AS is_approved,
                    room_id         AS room,
                    user_id         AS "user",
                    user_group_id   AS user_group,
                    tenant_id       AS tenant,
                    created_user_id AS created_user,
                    updated_user_id AS updated_user,
                    service_id      AS service
                FROM workorder
                WHERE tenant_id = %(tenant_id)s
                AND mrd_id = %(mrd_id)s
                AND is_delete = FALSE
            ) AS combined_results
            ORDER BY created_at DESC
            LIMIT %(limit)s
            OFFSET %(offset)s;
            """, {
                'tenant_id': tenant_id,
                'mrd_id': mrd_id,
                'limit': limit,
                'offset': offset
            }
        )
        return dictfetchall(cursor)