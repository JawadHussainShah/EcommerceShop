from attr import attr
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms

class RegistrationForm(UserCreationForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label='Confirm Password')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label='Password')
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control form-control-sm','autofocus':True}),
            'first_name': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'last_name': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class':'form-control form-control-sm','required':True}),
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs=
    {'autofocus':'true','class':'form-control'}))
    password = forms.CharField(label=_('Password'), 
    strip=False,widget=forms.PasswordInput(attrs={'class':'form-control'}))
        
class EditUserProfileForm(UserChangeForm):
    Password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login']

class EditAminProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = '__all__'
