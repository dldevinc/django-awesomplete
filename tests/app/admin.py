from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.timezone import now, timedelta
from taggit.forms import TagWidget
from taggit.models import Tag

from awesomplete.widgets import AwesompleteTagsWidgetWrapper, AwesompleteWidgetWrapper

from .models import City, CityLanguage, Person


def get_country_suggestions():
    return City.objects.values_list(
        'country', flat=True
    ).order_by('country').distinct()


def get_tag_suggestions():
    return Tag.objects.values_list(
        'name',
        flat=True
    ).order_by('name').distinct()


def get_language_suggestions():
    return CityLanguage.objects.values_list(
        'language', flat=True
    ).order_by('language').distinct()


class CityLanguageInlineForm(forms.ModelForm):
    class Meta:
        model = CityLanguage
        fields = forms.ALL_FIELDS
        widgets = {
            'language': AwesompleteWidgetWrapper(
                suggestions=get_language_suggestions
            )
        }


class CityLanguageInline(admin.TabularInline):
    model = CityLanguage
    form = CityLanguageInlineForm
    extra = 0


class CityLanguageStackedInline(admin.StackedInline):
    model = CityLanguage
    form = CityLanguageInlineForm
    extra = 0


class CityAdminForm(forms.ModelForm):
    class Meta:
        model = City
        fields = forms.ALL_FIELDS
        widgets = {
            'country': AwesompleteWidgetWrapper(
                suggestions=get_country_suggestions
            ),
            'tags': AwesompleteTagsWidgetWrapper(
                widget=TagWidget,
                suggestions=get_tag_suggestions
            )
        }


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    form = CityAdminForm
    inlines = (CityLanguageInline, CityLanguageStackedInline)
    list_display = ('name', 'country')


def date_generator():
    yield now() - timedelta(days=1), 'Yesterday'
    yield now(), 'Today'
    yield now() + timedelta(days=1), 'Tomorrow'


def date_formatter(dates):
    for datetime, label in dates:
        yield (
            datetime.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            ).strftime('%m/%d/%Y %H:%M:%S'),
            label
        )


def get_date_suggestions():
    """
    Example with chained generators
    """
    for date, label in date_formatter(date_generator()):
        yield {
            'label': label,
            'value': date
        }


class PersonForm(forms.ModelForm):
    date = forms.DateTimeField(
        required=False,
        label=Person._meta.get_field('date').verbose_name.capitalize(),
        help_text=Person._meta.get_field('date').help_text,
        widget=AwesompleteWidgetWrapper(
            widget=forms.DateTimeInput(attrs={
                'class': 'some-datetime-class'
            }),
            suggestions=get_date_suggestions,
            min_chars=0
        )
    )

    class Meta:
        model = Person
        fields = forms.ALL_FIELDS
        widgets = {
            'email': AwesompleteWidgetWrapper(
                widget=forms.EmailInput(attrs={
                    'class': 'some-email-class'
                }),
                min_chars=0,
                suggestions=(
                    'user@aol.com',
                    'user@mail.com',
                    'user@gmail.com',
                    'user@yahoo.com',
                    'user@hotmail.com',
                ),
            ),
            'language': AwesompleteWidgetWrapper(
                suggestions=settings.LANGUAGES
            )
        }


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = PersonForm
    list_display = ('name', 'email')
