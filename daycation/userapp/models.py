# userapp/models.py

from django.db import models

class userdb(models.Model):
    name = models.CharField(max_length=100)
    mobilenumber = models.CharField(max_length=15)
    emailid = models.EmailField()
    district = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    status = models.IntegerField(default=1)  # Assuming status is used for active/inactive

    def __str__(self):
        return self.username
