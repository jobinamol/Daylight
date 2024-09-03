from django.db import models

class UserDB(models.Model):
    name = models.CharField(max_length=255)
    mobilenumber = models.CharField(max_length=15)
    emailid = models.EmailField()
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    username = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg')
    password = models.CharField(max_length=128)  

    class Meta:
        db_table = 'users'
