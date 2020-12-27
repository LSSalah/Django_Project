from django.db import models
import re
from datetime import date,datetime
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
        if len(postData['birthday']) < 1:
            errors['birthday'] = "Date of Birth is required!"
        else:
            if datetime.strptime(postData['birthday'], "%Y-%m-%d") > datetime.today():
                errors['birthday'] = "Date of Birth must be in the past"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.IntegerField(null = True)
    address = models.CharField(max_length=255 , null = True)
    birthday = models.DateField(null = True)
    # role = models.ForeignKey(userRole, related_name = 'roles', on_delete = models.CASCADE)
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
    phone = models.IntegerField(null = True)
    address = models.CharField(max_length=255 , null = True)
    # car = models.CharField(max_length=255 , null = True)
    birthday = models.DateField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    
    def __repr__(self):
        return f"Name: {self.first_name} {self.last_name} | email : {self.email} "

class Order(models.Model):
    content = models.CharField(max_length = 255)
    poster = models.ForeignKey(User, related_name = 'orders', on_delete = models.CASCADE)
    deliver = models.ManyToManyField(Driver, related_name = "delivered")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

# class userRole(models.Model):
#     role = models.CharField(max_length=255)
