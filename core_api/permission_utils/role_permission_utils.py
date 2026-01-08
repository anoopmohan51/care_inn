from core_api.models.role_permission import RolePermission
from core_api.serializers.role_permission_serializer import RolePermissionSerializer
from core_api.models.permission import Permission
from django.db import transaction
from django.core import serializers

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
    update_ids = [r.get('id') for r in permission_data if r.get('id')]
    
    for record in permission_data:
        if not record.get('id'):
            to_create.append(RolePermission(
                role_id=record.get('role_id') or record.get('role'),
                permission_id=record.get('permission_id') or record.get('permission'),
                create=record.get('create', False),
                view=record.get('view', False),
                edit=record.get('edit', False),
                delete=record.get('delete', False)
            ))
    
    if update_ids:
        existing = RolePermission.objects.select_related('permission', 'role').filter(
            id__in=update_ids
        )
        instance_map = {inst.id: inst for inst in existing}
        
        for record in permission_data:
            record_id = record.get('id')
            if record_id and record_id in instance_map:
                inst = instance_map[record_id]
                inst.create = record.get('create', inst.create)
                inst.view = record.get('view', inst.view)
                inst.edit = record.get('edit', inst.edit)
                inst.delete = record.get('delete', inst.delete)
                to_update.append(inst)
    
    with transaction.atomic():
        created = RolePermission.objects.bulk_create(to_create) if to_create else []
        RolePermission.objects.bulk_update(to_update, ['create', 'view', 'edit', 'delete']) if to_update else None
    
    all_instances = list(to_update)
    if created:
        created_ids = [obj.id for obj in created if hasattr(obj, 'id') and obj.id]
        if created_ids:
            all_instances.extend(
                RolePermission.objects.select_related('permission', 'role').filter(id__in=created_ids)
            )
    
    return RolePermissionSerializer(all_instances, many=True).data
        