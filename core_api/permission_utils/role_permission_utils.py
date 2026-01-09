from core_api.models.role_permission import RolePermission
from core_api.serializers.role_permission_serializer import RolePermissionSerializer
from core_api.models.permission import Permission
from django.db import transaction
from django.core import serializers
from core_api.serializers.role_serializer import RoleListSerializer
from core_api.models.role import Role

def _create_update_role_permission(role_id,permission_data):
    permission_names = [record['name'] for record in permission_data]
    permissions = Permission.objects.filter(name__in=permission_names)
    permission_map = {permission.name: permission.id for permission in permissions}
    existing = {
        role_permission.permission_id:role_permission
            for role_permission in RolePermission.objects.filter(
            role_id=role_id,
            permission_id__in=permission_map.values()
        )
    }
    to_create = []
    to_update = []
    for record in permission_data:
        permission_id = permission_map.get(record['name'])
        if not permission_id:
            continue
        if permission_id in existing:
            update_obj = existing[permission_id]
            update_obj.create = record['create']
            update_obj.view = record['view']
            update_obj.edit = record['edit']
            update_obj.delete = record['delete']
            to_update.append(update_obj)
        else:
            to_create.append(RolePermission(
                role_id=role_id,
                permission_id=permission_id,
                create=record['create'],
                view=record['view'],
                edit=record['edit'],
                delete=record['delete']
            ))
    with transaction.atomic():
        created = RolePermission.objects.bulk_create(to_create)
        updated = RolePermission.objects.bulk_update(to_update,['create','view','edit','delete'])
    all_data = to_update + to_create
    all_data = RolePermissionSerializer(all_data,many=True).data
    return all_data

def _bulk_update_role_permission(permission_data):
    if not permission_data:
        return []
    to_create = []
    to_update = []
    role_ids = [record.get('id') or record.get('role') for record in permission_data]
    for record in permission_data:
        permissions = record.get('permission')
        for permission in permissions:
            if not permission.get('id'):
                to_create.append(RolePermission(
                    role_id=record.get('role_id') or record.get('role'),
                    permission_id=permission.get('permission_id') or permission.get('permission'),
                    create=permission.get('create', False),
                    view=permission.get('view', False),
                    edit=permission.get('edit', False),
                    delete=permission.get('delete', False)
                ))
            else:
                to_update.append(RolePermission(
                    id=permission.get('id'),
                    create=permission.get('create', False),
                    view=permission.get('view', False),
                    edit=permission.get('edit', False),
                    delete=permission.get('delete', False)
                ))
    with transaction.atomic():
        created = RolePermission.objects.bulk_create(to_create)
        updated = RolePermission.objects.bulk_update(to_update,['create','view','edit','delete'])
    roles = Role.objects.filter(id__in=role_ids,is_delete=False)
    role_data = RoleListSerializer(roles,many=True).data
    return role_data