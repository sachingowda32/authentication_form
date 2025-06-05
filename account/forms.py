from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class signupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2']   

class identifyuser(forms.Form):
    username = forms.CharField(max_length=50)
