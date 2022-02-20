from django.db import models

# Create your models here.

class Passports(models.Model):
    email = models.CharField(max_length=250, verbose_name="Email")
    passports = models.FileField(upload_to ='media/passports')