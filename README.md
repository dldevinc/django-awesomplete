# Django Awesomplete
A django app that provides suggestions while you type into the field.

[![PyPI](https://img.shields.io/pypi/v/django-awesomplete.svg)](https://pypi.org/project/django-awesomplete/)
[![Build Status](https://travis-ci.org/dldevinc/django-awesomplete.svg?branch=master)](https://travis-ci.org/dldevinc/django-awesomplete)

## Requirements
+ Python 3.4+
+ Django 1.11+

## Quickstart

Lets assume we are making a cities app in django and our `models.py` is:
```python
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name
```

To use suggestions we need to override widget in `admin.py`:
```python
from django import forms
from django.contrib import admin
from awesomplete.widgets import AwesompleteWidget
from .models import City


def get_country_suggestions():
    """
    Get a suggestions list from existing records.
    """
    return City.objects.values_list(
        'country', flat=True
    ).order_by('country').distinct()


class CityAdminForm(forms.ModelForm):
    class Meta:
        model = City
        fields = forms.ALL_FIELDS
        widgets = {
            'country': AwesompleteWidget(
                suggestions=get_country_suggestions
            )
        }


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    form = CityAdminForm
```

Result:

![](http://i.imgur.com/NRCdgNu.png)

## Installation
Install the desired version with pip:

```pip install django-awesomplete```

Then add awesomplete to INSTALLED_APPS in your settings file:

```python
INSTALLED_APPS = (
    # ...
    'awesomplete',
    # ...
)
```

## Suggestions
You can pass either an iterable of strings, 2-tuples, dicts or a callable that returns such an iterable.

```python
# iterable of strings
AwesompleteWidget(
    suggestions=['one', 'two', 'three']
)

# iterable of 2-tuples (label, value)
AwesompleteWidget(
    suggestions=(
        ('English', 'en'),
        ('Spanish', 'es')
    )
)

# iterable of dicts
AwesompleteWidget(
    suggestions=(
        {
            'label': 'English',
            'value': 'en'        
        },
        {
            'label': 'Spanish',
            'value': 'es'        
        }
    )
)
```

## Links
+ [awesomplete](http://leaverou.github.io/awesomplete/) created by Lea Verou.

## License
Copyright (c) 2018 Mihail Mishakin Released under the BSD license (see LICENSE)
