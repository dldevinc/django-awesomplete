# Django Awesomplete
A django app that provides suggestions while you type into the field.

[![PyPI](https://img.shields.io/pypi/v/django-awesomplete.svg)](https://pypi.org/project/django-awesomplete/)
[![Build Status](https://github.com/dldevinc/django-awesomplete/actions/workflows/tests.yml/badge.svg)](https://github.com/dldevinc/django-awesomplete)
[![Software license](https://img.shields.io/pypi/l/django-awesomplete.svg)](https://pypi.org/project/django-awesomplete/)

## Requirements
+ Python >= 3.6
+ Django >= 1.11

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

Let's assume we are making a cities app in django and our `models.py` is:
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
        'country', 
        flat=True
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

You can specify another widget explicitly, e.g. `EmailInput`:

```python
from django import forms
from awesomplete.widgets import AwesompleteWidgetWrapper
from .models import City


class CityAdminForm(forms.ModelForm):
    class Meta:
        model = City
        fields = forms.ALL_FIELDS
        widgets = {
            'email': AwesompleteWidgetWrapper(
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

You can also pass additional parameters to `AwesompleteWidgetWrapper`:

+ **`min_chars`**
  <br>
  Minimum characters the user has to type before the autocomplete 
  popup shows up.
  <br>
  *Default*: `1`

+ **`max_items`**
    <br>
    Maximum number of suggestions to display.
    <br>
    *Default*: `10`

+ **`autofirst`**
    <br>
    Should the first element be automatically selected?
    <br>
    *Default*: `True`

## AwesompleteTagsWidgetWrapper
This widget is a subclass of the `AwesompleteWidgetWrapper` and intended to be used
for entering comma-separated values. 

This widget can be used with [django-taggit](https://github.com/jazzband/django-taggit)

```python
from django import forms
from awesomplete.widgets import AwesompleteTagsWidgetWrapper
from taggit.models import Tag
from taggit.forms import TagWidget
from .models import City


def get_tag_suggestions():
    return Tag.objects.values_list(
        'name',
        flat=True
    ).order_by('name').distinct()


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = forms.ALL_FIELDS
        widgets = {
            'tags': AwesompleteTagsWidgetWrapper(
                widget=TagWidget,
                suggestions=get_tag_suggestions
            )
        }

```

![](https://i.imgur.com/zWAWhN7.png)

## Links
+ [awesomplete](http://leaverou.github.io/awesomplete/) created by Lea Verou.

## License
Copyright (c) 2018 Mihail Mishakin Released under the BSD license (see LICENSE)
