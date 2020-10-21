# Django Awesomplete
A django app that provides suggestions while you type into the field.

[![PyPI](https://img.shields.io/pypi/v/django-awesomplete.svg)](https://pypi.org/project/django-awesomplete/)
[![Build Status](https://travis-ci.org/dldevinc/django-awesomplete.svg?branch=master)](https://travis-ci.org/dldevinc/django-awesomplete)

## Requirements
+ Python 3.4+
+ Django 1.11+

## Installation
Install the desired version with pip:

```
pip install django-awesomplete
```

Then add awesomplete to INSTALLED_APPS in your settings file:

```python
INSTALLED_APPS = (
    # ...
    'awesomplete',
    # ...
)
```

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
from awesomplete.widgets import AwesompleteWidgetWrapper
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
            'country': AwesompleteWidgetWrapper(
                suggestions=get_country_suggestions
            )
        }


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    form = CityAdminForm
```

Result:

![](http://i.imgur.com/NRCdgNu.png)

## Suggestions
You can pass either an iterable of strings, 2-tuples, dicts 
or a callable that returns such an iterable.

```python
# iterable of strings
AwesompleteWidgetWrapper(
    suggestions=['one', 'two', 'three']
)

# iterable of 2-tuples (value, label)
AwesompleteWidgetWrapper(
    suggestions=(
        ('en', 'English'),
        ('es', 'Spanish')
    )
)

# iterable of dicts
AwesompleteWidgetWrapper(
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

## AwesompleteWidgetWrapper
Actually, `AwesompleteWidgetWrapper` is a wrapper for a widget. 
When the `widget` is not defined, it defaults to `TextInput`.

You can set `widget` explicitly:

```python
from django import forms
from awesomplete.widgets import AwesompleteWidgetWrapper
from .models import City


class CityAdminForm(forms.ModelForm):
    class Meta:
        model = City
        fields = forms.ALL_FIELDS
        widgets = {
            'email_awesomplete': AwesompleteWidgetWrapper(
                widget=forms.EmailInput,
                min_chars=0,
                suggestions=(
                    'noreply@mail.com',
                    'dont_disturb@mail.com',
                    'mayor@mail.com',
                    'support@mail.com',
                ),
            )
        }
```

## Links
+ [awesomplete](http://leaverou.github.io/awesomplete/) created by Lea Verou.

## License
Copyright (c) 2018 Mihail Mishakin Released under the BSD license (see LICENSE)
