from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from project.settings import MEDIA_DIR
from .models import *
from django import forms
from django.forms.widgets import TextInput
import math, os


class AccountForm(UserCreationForm):
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    username = forms.CharField(widget= TextInput(attrs={'class':'hidden'}),required=False)

    class Meta:
        model = User
        fields =  ['username','first_name','last_name','email','password1','password2']

    def clean_email(self): 
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        if not AllowedEmail.objects.filter(email=email).exists():
             raise ValidationError("This email does not have permissions to create an account")   
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name').replace(" ", "")
        if not str.isalpha(first_name):
            raise ValidationError("Enter a valid first name. This value may contain only letters")
        return self.cleaned_data.get('first_name')
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name').replace(" ", "")
        if not str.isalpha(last_name):
            raise ValidationError("Enter a valid last name. This value may contain only letters")
        return self.cleaned_data.get('last_name')


class UserInfoForm(UserChangeForm):
   
    email = forms.EmailField(disabled=True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    username = forms.CharField(widget= TextInput(attrs={'class':'hidden'}),required=False)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

    def clean_username(self):
        username = 'username'      
        return username 
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name').replace(" ", "")

        if not str.isalpha(first_name):
            raise ValidationError("Enter a valid first name. This value may contain only letters")
        return self.cleaned_data.get('first_name')
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name').replace(" ", "")

        if not str.isalpha(last_name):
            raise ValidationError("Enter a valid last name. This value may contain only letters")
        return self.cleaned_data.get('last_name')

        
class SocialMediaInfoForm(ModelForm):
    
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class':'class-off'}),required = False)

    class Meta:
        model = Account
        fields = '__all__'
        exclude = ['user', 'new_notifications']

    def clean_google_scholar(self):
        googleScholarLink = None
        if self.cleaned_data.get('google_scholar') is not None:
            googleScholarLink = self.cleaned_data.get('google_scholar')
            if "scholar.google" not in googleScholarLink.lower():
                raise ValidationError("This link is not valid")
        return googleScholarLink

    def clean_linkedin(self):
        linkedinLink = None
        if self.cleaned_data.get('linkedin') is not None:
            linkedinLink = self.cleaned_data.get('linkedin')
            if "linkedin" not in linkedinLink.lower():
                raise ValidationError("This link is not valid")
        return linkedinLink

    def clean_github(self):
        githubLink = None
        if self.cleaned_data.get('github') is not None:
            githubLink = self.cleaned_data.get('github')
            if "github" not in githubLink.lower():
                raise ValidationError("This link is not valid")
        return githubLink
