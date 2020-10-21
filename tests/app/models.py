from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    mayor_email = models.EmailField(blank=True)
    date = models.DateTimeField(null=True, blank=True, help_text="Select one of 'Yesterday', 'Today', 'Tomorrow'")

    def __str__(self):
        return self.name


class CityLanguage(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    language = models.CharField(max_length=255)

    def __str__(self):
        return self.language
