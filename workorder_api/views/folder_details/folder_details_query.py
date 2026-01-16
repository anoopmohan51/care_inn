from django.db import connection
from workorder_api.views.workorder_dashboard.workorder_count_per_day import dictfetchall
def _get_folder_details(tenant_id,folder_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT
                    jsonb_build_object(
                        'id', f.id,
                        'name', f.name,
                        'folder_id', f.id,
                        'workorder_settings_id', f.workorder_settings_id,
                        'folder_details',
                        (
                            SELECT jsonb_agg(details)
                            FROM (
                                -- Sub folders
                                SELECT jsonb_build_object(
                                    'id', sf.id,
                                    'name', sf.name,
                                    'type', 'FOLDER',
                                    'folder_id', sf.parent_folder_id,
                                    'workorder_settings_id', sf.workorder_settings_id,
                                    'icon', sf.icon,
                                    'color', sf.color,
                                    'static_files', sf.static_file_id 
                                ) AS details
                                FROM workorder_api_folder sf
                                WHERE sf.parent_folder_id  = f.id

                                UNION ALL

                                -- Informations
                                SELECT jsonb_build_object(
                                    'id', i.id,
                                    'name', i.information,
                                    'type', 'INFORMATION',
                                    'folder_id', i.folder_id,
                                    'workorder_settings_id', i.workorder_settings_id,
                                    'icon', i.icon,
                                    'static_files', i.static_file_id 
                                )
                                FROM workorder_api_informations i
                                WHERE i.folder_id = f.id

                                UNION ALL

                                -- Requested Items
                                SELECT jsonb_build_object(
                                    'id', r.id,
                                    'name', r.name,
                                    'type', 'REQUEST',
                                    'folder_id', r.folder_id,
                                    'workorder_settings_id', r.workorder_settings_id,
                                    'icon', r.icon,
                                    'color', r.color,
                                    'static_files', r.static_file_id 
                                )
                                FROM workorder_api_requested_items r
                                WHERE r.folder_id = f.id

                                UNION ALL

                                -- Services
                                SELECT jsonb_build_object(
                                    'id', s.id,
                                    'name', s.name,
                                    'type', 'SERVICE',
                                    'folder_id', s.folder_id,
                                    'workorder_settings_id', s.workorder_settings_id,
                                    'icon', s.icon,
                                    'color', s.color,
                                    'static_files', s.static_file_id 
                                )
                                FROM workorder_api_services s
                                WHERE s.folder_id = f.id
                            ) t
                        )
                    ) AS result
                FROM workorder_api_folder f
                WHERE f.id = %s;
                """, [folder_id]
        )
        print(cursor.fetchall())
        # return dictfetchall(cursor)