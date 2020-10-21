from django.db import models
from django.conf import settings


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CityLanguage(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    language = models.CharField(max_length=255)

    def __str__(self):
        return self.language


class Person(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    date = models.DateTimeField(null=True, blank=True, help_text="Select one of 'Yesterday', 'Today', 'Tomorrow'")
    language = models.CharField(choices=settings.LANGUAGES, max_length=64, blank=True)

    def __str__(self):
        return self.name
