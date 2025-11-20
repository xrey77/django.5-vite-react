from django.db import models
from .storages import NoOpStorage

class Users(models.Model):
    firstname   = models.CharField(max_length=215, blank=True, null=True)
    lastname    = models.CharField(max_length=215, blank=True, null=True)
    email       = models.CharField(max_length=215)
    mobile      = models.CharField(max_length=215, blank=True, null=True)
    username    = models.CharField(max_length=215)
    password    = models.CharField(max_length=215)
    roles       = models.CharField(max_length=215, null=True)
    userpic     = models.ImageField(upload_to='users/', blank=True, null=True)
    # userpic     = models.ImageField(upload_to='users/', default='http://127.0.0.1:8000/media/images/pix.png', null=True, blank=True)
    secret      = models.CharField(max_length=215, blank=True, null=True)
    qrcodeurl   = models.ImageField(storage=NoOpStorage(), upload_to='qrcodes/', null=True, blank=True)    
    isblocked   = models.BooleanField(default=False)    
    isactivated = models.BooleanField(default=False)
    mailtoken   = models.IntegerField(default=0)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    # def __str__(self):
    #     return f"User object created at {self.created_at}, last updated at {self.updated_at}"
    
    
