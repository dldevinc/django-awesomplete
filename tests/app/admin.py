from django import forms
from django.contrib import admin
from django.utils.timezone import now, timedelta
from awesomplete.widgets import AwesompleteWidget
from .models import City, CityLanguage


def get_country_suggestions():
    return City.objects.values_list(
        'country', flat=True
    ).order_by('country').distinct()


def get_language_suggestions():
    return CityLanguage.objects.values_list(
        'language', flat=True
    ).order_by('language').distinct()


def date_generator():
    yield 'Yesterday', now() - timedelta(days=1)
    yield 'Today', now()
    yield 'Tomorrow', now() + timedelta(days=1)


def date_formatter(dates):
    for name, datetime in dates:
        yield (
            name,
            datetime.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            ).strftime('%m/%d/%Y %H:%M:%S')
        )


def get_date_suggestions():
    """
    Example with chained generators
    """
    for label, date in date_formatter(date_generator()):
        yield {
            'label': label,
            'value': date
        }


class CityLanguageInlineForm(forms.ModelForm):
    class Meta:
        model = CityLanguage
        fields = forms.ALL_FIELDS
        widgets = {
            'language': AwesompleteWidget(
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
    date = forms.DateTimeField(
        required=False,
        label=City._meta.get_field('date').verbose_name.capitalize(),
        help_text=City._meta.get_field('date').help_text,
        widget=AwesompleteWidget(
            suggestions=get_date_suggestions,
            min_chars=0
        )
    )

    class Meta:
        model = City
        fields = forms.ALL_FIELDS
        widgets = {
            'country': AwesompleteWidget(
                suggestions=get_country_suggestions
            ),
        }


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    form = CityAdminForm
    inlines = (CityLanguageInline, CityLanguageStackedInline)
    list_display = ('name', 'country')
