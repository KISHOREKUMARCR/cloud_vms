
from django.db import models

# Create your models here.
class Roles(models.Model):

    role_name = models.CharField(max_length=50)
    role_description = models.CharField(max_length=200)
    role_status = models.BooleanField(default=True)

    def __str__(self):
        return self.role_name

class UserSocialAccount(models.Model):
    name = models.CharField(max_length=60, null=True)
    user_name = models.CharField(max_length=60, null=True)
    user_email = models.CharField(max_length=100, null=True)
    user_mobile = models.CharField(max_length=15,null=True)
    user_image_url = models.CharField(max_length=500, null=True)    
    user_social_provider = models.CharField(max_length=50, null=True)
    #user_is_new = models.CharField(max_length=60)
    user_roles = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    user_status = models.BooleanField(default=True)
    user_company_name = models.CharField(max_length=100,null=True)
    user_business_type = models.CharField(max_length=100,null=True)
    
    user_description = models.CharField(max_length=200,null = True)
    user_country = models.CharField(max_length = 50,null = True)
    user_state = models.CharField(max_length = 50,null = True)
    user_city = models.CharField(max_length = 50,null = True)
    
    def __str__(self):
        return self.user_name
    


class UserAccount(models.Model):

    name = models.CharField(max_length=60,)
    user_name = models.CharField(max_length=60)
    user_email = models.CharField(max_length=100)
    user_mobile = models.CharField(max_length=15,null=True)
    user_roles = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
    user_password = models.CharField(max_length=20,null=True)
    user_company_name = models.CharField(max_length=100,null=True)
    user_business_type = models.CharField(max_length=100,null=True)
    #user_confirm_password = models.CharField(max_length=20)
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    user_status = models.BooleanField(default=True)
    
    user_image = models.ImageField(upload_to='profile_image', blank=True)
    user_description = models.CharField(max_length=200,null = True)
    user_country = models.CharField(max_length = 50,null = True)
    user_state = models.CharField(max_length = 50,null = True)
    user_city = models.CharField(max_length = 50,null = True)
    
    #for g-Auth
    user_image_url = models.CharField(max_length=500, null=True)    
    user_social_provider = models.CharField(max_length=50, null=True)
    user_profile_update = models.DateField(auto_now_add=True,null=True)
    pre_last_login = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.user_name}_{self.id}'
    
    @property
    def is_authenticated(self):
        pass
    
    @is_authenticated.setter
    def is_authenticated(self):
        pass
    


