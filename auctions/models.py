from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin

class auctionAdmin(admin.ModelAdmin):
    list_display= ("id", "title", "image", "startingPrice")

class User(AbstractUser):
    pass 

class auctionList(models.Model):
    title = models.CharField(max_length=64)
    startingPrice = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=500, default=None, blank=True, null=True)
    description = models.CharField(max_length=100, default="Enter description here.")
    catagory = models.CharField(max_length=100, default='Other', choices=[('other', 'Other'), \
        ('fashion', 'Fashion'), ('toys', 'Toys'), ('electronics', 'Electronics'), ('home', 'Home')])
    user = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=100, default="Open")
    winner = models.CharField(max_length=64, null=True, blank=True)

class newItem(models.Model):
    title = models.CharField(max_length=64)
    startingPrice = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=500, default=None, blank=True, null=True)
    description = models.CharField(max_length=100, default="Enter description here.")
    catagory = models.CharField(max_length=100, default='Other', choices=[('other', 'Other'), \
        ('fashion', 'Fashion'), ('toys', 'Toys'), ('electronics', 'Electronics'), ('home', 'Home')])
    user = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=100, default="Open")
    winner = models.CharField(max_length=64, null=True, blank=True)

class watchlist(models.Model):
    user =  models.CharField(max_length=64)
    auction = models.IntegerField(null=True)

class bids(models.Model):
    user = models.CharField(max_length=64, blank=True, null=True)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    auction_item = models.IntegerField(null=True)

class comments(models.Model):
    user = models.CharField(max_length=64, blank=True, null=True)
    comment = models.CharField(max_length=500, null=True, blank=True)
    auction_item = models.IntegerField(null=True, blank=True)
