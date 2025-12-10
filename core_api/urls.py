from django.urls import path
from .views.users.users import *
from .views.login.user_login import *
from .views.tenant.tenant import *
urlpatterns = [
    path('user',UserCreateView.as_view()),
    path('user/<int:pk>',UserUpdateView.as_view()),
    path('change-password/<int:pk>',UserResetPasswordView.as_view()),
    path('login',UserLoginView.as_view()),
    path('tenant',TenantCreateView.as_view()),
]