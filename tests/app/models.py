from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
