from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

from .models import User
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name"]
class UserCreation(UserCreationForm):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(), required=False)    
    class Meta:
        model = User
        fields = ["email" ,"username" ,"first_name","last_name" ,"password1","password2" ,"company"]
        
    widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ism"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Familiya"}),
          
            "password1": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parol"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parolni tasdiqlang"}),
        }
class CompanyID(forms.Form):
    code = forms.IntegerField(
        min_value=1000,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Korxona raqamini kiriting"})
    )
class WorkerForm(forms.Form):
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ism"}))
    last_name = forms.CharField(max_length=100,
                                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Familiya"}))
class UserCreationWorker(UserCreationForm):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(), required=False)
    
    class Meta:
        model = User
        fields = ["email" ,"username" ,"password1","password2" ,"company"]
        
    widgets = {
           
            "password1": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parol"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parolni tasdiqlang"}),
        }
