from django.db import connection
from workorder_api.views.workorder_dashboard.workorder_count_per_day import dictfetchall
def _get_folder_details(folder_id,limit,offset):

    with connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT
                    f.id::integer,
                    NULL::text AS created_user_name,
                    f.color::text,
                    f.icon::text,
                    f.static_file_id::uuid,
                    f.id::integer AS folder_id,
                    f.workorder_settings_id,
                    f.name::text,
                    'FOLDER'::text AS type,
                    NULL::integer AS service_id,
                    NULL::integer AS item_id,
                    NULL::integer AS information_id,
                    NULL::integer AS request_id,
                    FALSE::boolean AS is_delete,
                    NULL::timestamp AS created_at,
                    NULL::timestamp AS updated_at,
                    NULL::integer as tenant_id,
                    NULL::integer AS created_user_id,
                    NULL::integer AS updated_user_id,
                    f.position ::integer,
                    f.name_arabic::text
                FROM workorder_api_folder f
                WHERE f.parent_folder_id = %(folder_id)s

                UNION ALL

                SELECT
                    s.id::integer,
                    NULL::text,
                    s.color::text,
                    s.icon::text,
                    s.static_file_id::uuid,
                    s.folder_id::integer,
                    s.workorder_settings_id,
                    s.name::text,
                    'SERVICE'::text,
                    s.id::integer,
                    NULL::integer,
                    NULL::integer,
                    NULL::integer,
                    s.is_delete::boolean,
                    s.created_at::timestamp,
                    s.updated_at::timestamp,
                    s.tenant_id,
                    s.created_user_id,
                    s.updated_user_id,
                    s.position ::integer,
                    s.name_arabic::text 
                FROM workorder_api_services s
                WHERE s.folder_id = %(folder_id)s

                UNION ALL

                SELECT
                    r.id::integer,
                    NULL::text,
                    r.color::text,
                    r.icon::text,
                    NULL::uuid AS static_file_id,
                    r.folder_id::integer,
                    r.workorder_settings_id,
                    r.name::text,
                    'REQUEST'::text,
                    NULL::integer,
                    NULL::integer,
                    NULL::integer,
                    r.id::integer,
                    r.is_delete::boolean,
                    r.created_at::timestamp,
                    r.updated_at::timestamp,
                    r.tenant_id,
                    r.created_user_id,
                    r.updated_user_id,
                    r.position ::integer,
                    r.name_arabic::text
                FROM workorder_api_requested_items r
                WHERE r.folder_id = %(folder_id)s

                UNION ALL

                SELECT
                    i.id::integer,
                    NULL::text,
                    NULL::text,
                    i.icon::text,
                    i.static_file_id::uuid,
                    i.folder_id::integer,
                    i.workorder_settings_id,
                    i.title::text,
                    'INFORMATION'::text,
                    NULL::integer,
                    NULL::integer,
                    i.id::integer,
                    NULL::integer,
                    i.is_delete::boolean,
                    i.created_at::timestamp,
                    i.updated_at::timestamp,
                    i.tenant_id,
                    i.created_user_id,
                    i.updated_user_id,
                    i.position ::integer,
                    i.title_arabic::text AS name_arabic
                FROM workorder_api_informations i
                WHERE i.folder_id = %(folder_id)s
                ORDER BY position ASC
                LIMIT %(limit)s OFFSET %(offset)s
                """,{
                    "folder_id":folder_id,
                    "limit":limit,
                    "offset":offset
                }
                
        )
        return dictfetchall(cursor)