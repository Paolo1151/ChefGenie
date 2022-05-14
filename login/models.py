from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User


class AccountManager(BaseUserManager):
    def create_user(self, email_address, username, password=None):
        if not email_address:
            raise ValueError('User must have an email address.')
        if not username:
            raise ValueError('User must have a username.')

        user = self.model(
            email_address = self.normalize_email(email_address),
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, username, password):
        user = self.create_user(
            email_address = self.normalize_email(email_address),
            username = username,
            password = password
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email_address = models.EmailField(verbose_name="email_address", unique=True)
    username = models.CharField(verbose_name="username", max_length=30, unique=True)
    
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email_address']

    objects = AccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserAccount(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    weight = models.DecimalField(verbose_name="weight", max_digits=5, decimal_places=2, default=60.00)
    height = models.DecimalField(verbose_name="height", max_digits=5, decimal_places=2, default=160.00)
    weight_goal = models.DecimalField(max_digits=5, decimal_places=2, default=60.00)
    calorie_goal = models.IntegerField(default=2500)
    profile_picture = models.ImageField(null="/media/profile_pictures/default.jpg ", blank=True, upload_to="profile_pictures/")

    @property
    def bmi(self):
        return self.weight / (self.height**2 / 10000)

    def change_values(self, nweight, nheight, nweight_goal, ncalorie_goal):
        weight = nweight
        height = nheight
        weight_goal = nweight_goal
        calorie_goal = ncalorie_goal