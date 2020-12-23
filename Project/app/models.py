from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if (len(postData['first_name']) < 1) or (len(postData['last_name']) < 1) or (len(postData['email']) < 1):
            errors["blank"] = "All fields are required and must not be empty!"
        if not (postData['first_name'].isalpha() and postData['last_name'].isalpha()):
            errors["alpha"] = "First and Last Name cannot contain any numbers!"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email Address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if postData['passwordconfirmation'] != postData['password']:
            errors['passwordconfirmation'] = "Confirmation password does not match password!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.IntegerField()
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    
    def __repr__(self):
        return f"Name: {self.first_name} {self.last_name} | email : {self.email} "


class Driver(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.IntegerField()
    address = models.CharField(max_length=255)
    car = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    
    def __repr__(self):
        return f"Name: {self.first_name} {self.last_name} | email : {self.email} "