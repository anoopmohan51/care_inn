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
                    temp.id,
                    temp.workorder_type,
                    temp.assignee_type,
                    temp.description,
                    temp.priority,
                    temp.when_to_start,
                    temp.sla_minutes,
                    temp.mrd_id,
                    temp.status,
                    temp.created_at,
                    temp.updated_at,
                    temp.is_delete,
                    temp.unique_id,
                    temp.source,
                    temp.start_date,
                    temp.end_date,
                    temp.is_approved,
                    temp.room_id         AS room,
                    temp.user_id         AS "user",
                    temp.user_group_id   AS user_group,
                    temp.tenant_id       AS tenant,
                    temp.created_user_id AS created_user,
                    temp.updated_user_id AS updated_user,
                    temp.service_id      AS service,
                    s.name               AS service_name,
                    s.name_arabic        AS service_name_arabic
                FROM workorder_temp temp
                LEFT JOIN workorder_api_services s
                    ON s.id = temp.service_id
                WHERE temp.tenant_id = %(tenant_id)s
                AND temp.mrd_id =  %(mrd_id)s
                AND temp.is_delete = FALSE
                AND temp.is_approved = FALSE

                UNION ALL

                /* ---------- workorder ---------- */
                SELECT
                    wo.id,
                    wo.workorder_type,
                    wo.assignee_type,
                    wo.description,
                    wo.priority,
                    wo.when_to_start,
                    wo.sla_minutes,
                    wo.mrd_id,
                    wo.status,
                    wo.created_at,
                    wo.updated_at,
                    wo.is_delete,
                    wo.unique_id,
                    wo.source,
                    wo.start_date,
                    wo.end_date,
                    TRUE                AS is_approved,
                    wo.room_id          AS room,
                    wo.user_id          AS "user",
                    wo.user_group_id    AS user_group,
                    wo.tenant_id        AS tenant,
                    wo.created_user_id  AS created_user,
                    wo.updated_user_id  AS updated_user,
                    wo.service_id       AS service,
                    s.name              AS service_name,
                    s.name_arabic       AS service_name_arabic
                FROM workorder wo
                LEFT JOIN workorder_api_services s
                    ON s.id = wo.service_id
                WHERE wo.tenant_id =  %(tenant_id)s
                AND wo.mrd_id = %(mrd_id)s
                AND wo.is_delete = FALSE
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