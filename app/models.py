from pyexpat import model
from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    description = models.TextField(max_length=400)
    
    def __str__(self):
        return f'Message from {self.name}'

class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    authname = models.CharField(max_length=50)
    img = models.ImageField(upload_to='pics', blank=True, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Uploaded by {self.authname}'

class Subscribe(models.Model):
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)