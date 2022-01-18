from django import forms

from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Create_user_form(UserCreationForm):
    GENDER_CHOICES = [('M','Male'),('F','Female')]
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.RadioSelect)
    

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2','gender']

        widgets = {
            'username' :forms.TextInput(attrs ={'name':'username'})  ,
            'email' :forms.EmailInput(attrs ={'name':'email'}),
            'password1' :forms.PasswordInput(attrs ={'name':'password'}),
            'first_name' :forms.TextInput(attrs ={'name':'firstname'}),
            'last_name' :forms.TextInput(attrs ={'name':'lastname'}),
        }


    def clean(self):
        all = super().clean()
        email = all['email']
        gender = all['gender']
        username = all['username']
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken , choose another")
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError(str(email) + " is already used , use another")
        if gender not in ['M', 'F']:
            raise forms.ValidationError("Gender error , don't tamper with data")