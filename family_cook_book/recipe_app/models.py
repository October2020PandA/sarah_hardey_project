from django.db import models
from django.forms import ModelForm
import bcrypt
import re 

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) == 0:
            errors['first_name'] = "First name is required." 
        elif len(postData['first_name']) < 2 or postData['first_name'].isalpha() != True:
            errors['first_name'] = "First name must be at least 2 charcters long and only use letters."
        if len(postData['last_name']) == 0:
            errors['last_name'] = "Last name is required." 
        elif len(postData['last_name']) < 2 or postData['last_name'].isalpha() != True:
            errors['last_name'] = "Last name must be at least 2 charcters long and only use letters."
        if len(postData['email']) == 0:
            errors['email'] = "Email is required."
        if not email_regex.match(postData['email']):
            errors['email'] = "Invalide format for an email."
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) > 0:
            errors['email'] = "Email already in use."
        if len(postData['password']) == 0:
            errors['password'] = "Password is required."
        elif len(postData['password']) < 8 :
            errors['password'] = "Pasword myst be at least 8 characters long."
        elif postData['password'] != postData['confirm_pw']:
            errors['password'] = "Password and Confirm Password do not match, please try again."
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) == 0:
            errors['email'] = "Email is required."
        elif not email_regex.match(postData['email']):
            errors['email'] = "Invalid email address."
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) != 1: 
            errors['email'] = "Email and password are required. Please try again. "
        elif len(postData['password']) < 8: 
            errors['password'] = "Password must be at least 8 characters."
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['password'] = "Email and Password do no match. Please try again."
        return errors

class RecipeManager(models.Manager):
    def recipe_validator(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors['title'] = "Recipe title is required."
        elif len(postData['title']) < 3:
            errors['title'] = "Your recipe  title  must be at least 3 characters."
        if len(postData['ingredents']) == 0:
            errors['ingredents'] = "Recipe ingredents are required."
        elif len(postData['ingredents']) < 5:
            errors['ingredents'] = "Your recipe ingredents must be at least 5 characters."
        if len(postData['instructions']) == 0:
            errors['instructions'] = "Recipe instructions are required."
        elif len(postData['instructions']) < 10:
            errors['instructions'] = "Your recipe instructions must be at least 10 characters."
        return errors
        #adding an image is OPTIONAL; no validator needed.
        if len(postData['image']) == 0:
            errors['image'] = "An image must be included."

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()

class Recipe(models.Model):
    title = models.CharField(max_length=225)
    ingredents = models.TextField()
    instructions = models.TextField()
    # brief_dis = models.CharField(max_length=100) 
    recipe_creator = models.ForeignKey(User, related_name="chef", on_delete = models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    liked_by = models.ManyToManyField(User, related_name="liked_recipes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RecipeManager()

class Comment(models.Model):
    comment_text = models.TextField()
    comment_user = models.ForeignKey(User, related_name="commenter", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recipe_comment = models.ForeignKey(Recipe, related_name="post_comments", on_delete=models.CASCADE)
