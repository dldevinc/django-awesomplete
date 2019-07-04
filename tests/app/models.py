from django.db import models


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
