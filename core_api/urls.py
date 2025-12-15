from django.urls import path
from .views.users.users import *
from .views.login.user_login import *
from .views.tenant.tenant import *
from .views.user_group.user_group import *
from .views.role.role import *
from .views.user_permission.user_permission import *
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
    path('user-permission/<int:pk>',UserPermissionDetailView.as_view()),

]