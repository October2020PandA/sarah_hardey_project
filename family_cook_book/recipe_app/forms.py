from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Recipe
 
class NewUserForm(UserCreationForm):
    #password (password1), confirm password (password2), and user name are default
    first_name = forms.CharField(max_length=60,required=True)
    last_name = forms.CharField(max_length=60,required=True)
    email = forms.EmailField(required=True)
    class Meta: 
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2") #order that fields are displayed

class NewRecipeForm(forms.ModelForm):
    # title = forms.CharField(max_length=225, required=True)
    # ingredents = forms.TextField(required=True)
    # instructions = forms.TextField(required=True)
    # image = forms.ImageField(upload_to='images/', blank=True, required=True)
    class Meta: 
        model = Recipe
        fields = ("title", "ingredents", "instructions", "image")
