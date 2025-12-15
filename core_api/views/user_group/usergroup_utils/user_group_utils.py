from core_api.models.usergroups import UserGroup,UserGroupUsers
from core_api.serializers.usergroup_serializer import UserGroupSerializer
from django.db import transaction
from django.db.models import F,Value
from django.db.models.functions import Concat

class UserGroupUsersService:
    # @transaction
    def get_user_group_users(self,data,user_group_id):
        user_ids=[record['id'] for record in data]
        existing_records=list(UserGroupUsers.objects.filter(
            user_group_id=user_group_id
        ).values_list('user_id',flat=True))
        existing_user_ids=set(existing_records)
        new_user_ids=set(user_ids)
        to_delete_ids=existing_user_ids-new_user_ids
        if to_delete_ids:
            UserGroupUsers.objects.filter(
                user_group_id=user_group_id,
                user_id__in=to_delete_ids
            ).delete()
        to_add_ids=new_user_ids-existing_user_ids
        if to_add_ids:
            UserGroupUsers.objects.bulk_create(
                [UserGroupUsers(user_group_id=user_group_id,user_id=user_id) for user_id in to_add_ids]
            )
    def delete_whole_user_group(self,user_group_id):
        UserGroupUsers.objects.filter(user_group_id=user_group_id).delete()
    
    def get_user_group_users_list(self,user_group_id):
        fields=['id','user']
        queryset=UserGroupUsers.objects.filter(
            user_group_id=user_group_id
        ).values(*fields).annotate(
            user_full_name=Concat(F('user__first_name'),Value(' '),F('user__last_name')),
            user_email=F('user__email'),
            user_status=F('user__status'),
            user_created_at=F('user__created_at'),
            user_updated_at=F('user__updated_at'),
            user_tenant=F('user__tenant'),
            user_is_delete=F('user__is_delete'),
            user_position=F('user__position'),
            user_role=F('user__role'),
        )
        response = []
        for record in queryset:
            response.append({
                'id':record['id'],
                'user_full_name':record['user_full_name'],
                'user_email':record['user_email'],
                'user_status':record['user_status'],
                'user_created_at':record['user_created_at'],
                'user_updated_at':record['user_updated_at'],    
                'user_tenant':record['user_tenant'],
                'user_is_delete':record['user_is_delete'],
                'user_role':record['user_role'],
            })
        return response


        
