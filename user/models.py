from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, is_active=True, is_staff=False, is_admin=False):
        if not username:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            username = username,
            password = password,
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username, password=None):
        user = self.create_user(
                username,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
                username,
                password=password,
                is_staff=True,
                is_admin=True
        )
        return user



class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255)
    city   = models.CharField(max_length=255, blank=True, null=True)
    address   = models.CharField(max_length=255, blank=True, null=True)
    username   = models.CharField(max_length=255, blank=False, null=False,unique=True)
    contact   = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=50)
    userrole = (('Admin','Admin'),('User','User'))
    role = models.CharField(max_length=50,blank=False, null=False, choices = userrole,default = 'User')
    
    is_active   = models.BooleanField(default=True) # can login 
    staff       = models.BooleanField(default=False) # staff user non superuser
    admin       = models.BooleanField(default=False) # superuser 


    USERNAME_FIELD = 'username' 

    REQUIRED_FIELDS = ['password'] 

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # userrole = (('Admin','Admin'),('User','User'))
    # role = models.CharField(max_length=50,blank=False, null=False, choices = userrole,default = 'User')
    
    # class Meta:
    #     ordering = ('-salary',)

    def __str__(self):
        return "{0} {1}".format(self.user.username, self.user.role)


@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    print(created)
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()