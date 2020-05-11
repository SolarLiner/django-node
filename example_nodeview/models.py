from django.db import models


# Create your models here.

class House(models.Model):
    address = models.CharField(max_length=255)


class Person(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=60)
    houses = models.ManyToManyField(House, related_name="owners", blank=True)
