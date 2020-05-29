from django.db import models
from django import forms

# Create your models here.
class Product(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.name
