from django.db import connection
from workorder_api.views.workorder_dashboard.workorder_count_per_day import dictfetchall
def _get_folder_details(tenant_id,folder_id):

    with connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT
                    f.id,
                    f.color,
                    f.icon,
                    f.static_file_id,
                    f.id AS folder_id,
                    f.workorder_settings_id,
                    f.name,
                    'FOLDER' AS type
                FROM workorder_api_folder f
                WHERE f.parent_folder_id = %s

                UNION ALL

                SELECT
                    s.id,
                    s.color,
                    s.icon,
                    s.static_file_id ,
                    s.folder_id,
                    s.workorder_settings_id,
                    s.name,
                    'SERVICE' AS type
                FROM workorder_api_services s
                WHERE s.folder_id = %s

                UNION ALL

                SELECT
                    r.id,
                    r.color,
                    r.icon,
                    null as static_file,
                    r.folder_id,
                    r.workorder_settings_id,
                    r.name,
                    'REQUEST' AS type
                FROM workorder_api_requested_items r
                WHERE r.folder_id = %s

                UNION ALL

                SELECT
                    i.id,
                    null as color,
                    i.icon,
                    i.static_file_id ,
                    i.folder_id,
                    workorder_settings_id,
                    i.information ,
                    'INFORMATION' AS type
                FROM workorder_api_informations i
                WHERE i.folder_id = %s

                """,[folder_id,folder_id,folder_id,folder_id]
        )
        return dictfetchall(cursor)