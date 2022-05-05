from operator import mod
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    userprofile = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to = 'images/',
        blank = True,
        null = True,
    )

    def __str__(self):
        return self.userprofile.username

class Category(models.Model):
    title = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(
        upload_to = 'images/',
    )
    market_price = models.PositiveIntegerField()
    selling_price = models.PositiveSmallIntegerField()
    description = models.TextField(max_length=400)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
