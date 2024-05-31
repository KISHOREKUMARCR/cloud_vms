from django import forms
from django.contrib.auth.models import User
from accounts.models import *

from captcha.fields import CaptchaField,CaptchaTextInput

class UserAccountForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = UserAccount
        fields= ['name','user_email','user_mobile','user_name','user_password']
        labels = {
                'name':'Name',
                'user_name': 'User Name',
                'user_email': 'Email',
                'user_mobile': 'Mobile',
                'user_password': 'Password',
        }
        widgets = {
            'name' : forms.TextInput(attrs = {'class':'form-control','id':'name','placeholder':'Enter Your Name'}),
            'user_name' : forms.TextInput(attrs = {'class':'form-control','id':'username','placeholder':'Enter Username'}),
            #'user_roles' : forms.Select(attrs = {'class':'form-control'}),
            'user_email' : forms.EmailInput(attrs = {'class':'form-control','id':'email','placeholder':'Enter Your Email ID'}),
            'user_mobile' : forms.TextInput(attrs = {'class':'form-control','id':'mobile','placeholder':'Enter Your Mobile No'}),
            'user_password' : forms.PasswordInput(attrs = {'class':'form-control','placeholder':'Enter Password'}),
            #'user_confirm_password' : forms.PasswordInput(attrs = {'class':'form-control','placeholder':'Comfirm Password'}),
            }

class UserAccountUpdateForm(forms.ModelForm):

    class Meta:
        model = UserAccount
        fields = ['user_name','user_roles','user_email','user_mobile']

		
class CaptchaForms(forms.Form):
    captcha=CaptchaField(widget=CaptchaTextInput(attrs={'class': 'form-control','style':'margin-top: 10px;'}))
    #captcha=CaptchaField(label='Please enter the characters in the image')#,'width: 300px;','height: 10px;'}))
       