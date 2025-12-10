from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from core_api.models.position import Position
from core_api.models.role import Role
from core_api.models.tenant import Tenant

class UserManager(BaseUserManager):
    def create_user(
        self, 
        email,
        password,
        first_name,
        last_name=None,
        address=None,
        city=None,
        state=None,
        country=None,
        phone=None,
        designation=None,
        position=None,
        role=None,
        tenant=None,
        status=True,
        created_at=None,
        updated_at=None,
        is_delete=False
    ):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            state=state,
            country=country,
            phone=phone,
            designation=designation,
            position=position,
            role=role,
            tenant=tenant,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            is_delete=is_delete
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class AppUsers(AbstractBaseUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255,null=True)
    email = models.EmailField(max_length=255,null=True,unique=True)
    address=models.TextField(null=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)
    country = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=10,null=True)
    designation = models.CharField(max_length=50,null=True)
    position = models.ForeignKey(Position, on_delete=models.PROTECT,null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT,null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email
    
    @property
    def is_superuser(self):
        return self.role.name == 'SUPERADMIN'