from django.urls import path
from .views.users.users import *
from .views.login.user_login import *
from .views.tenant.tenant import *
from .views.user_group.user_group import *
from .views.role.role import *
from .views.external_api_key.external_api_key import *
from .views.role.role_permission import *
from .views.role_permission.permission import *
from .views.user_group.list_users import *
urlpatterns = [
    path('user',UserCreateView.as_view()),
    path('user/<int:pk>',UserUpdateView.as_view()),
    path('change-password/<int:pk>',UserResetPasswordView.as_view()),
    path('user/filter',UserFilterView.as_view()),
    path('login',UserLoginView.as_view()),
    path('tenant',TenantCreateView.as_view()),
    path('user-group',UserGroupCreateView.as_view()),
    path('user-group/<int:pk>',UserGroupDetialsView.as_view()),
    path('user-group/filter',UserGroupFilterView.as_view()),
    path('user-group/users/<int:pk>',UserGroupUsersDeleteView.as_view()),
    path('role',RoleCreateView.as_view()),
    path('role/<int:pk>',RoleDetailsView.as_view()),
    path('role/filter',RoleFilterView.as_view()),
    path('refresh-token',TokenRefreshView.as_view()),
    path('generate-external-api-key',ExternalApiKeyCreateView.as_view()),
    path('role-permission/bulk-update',RolePermissionBulkUpdateView.as_view()),
    path('list-permission',PermissionListView.as_view()),
    path('list-users',ListUsersView.as_view()),

]