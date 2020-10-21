from django import forms
from django.contrib import admin
from django.utils.timezone import now, timedelta
from awesomplete.widgets import AwesompleteWidgetWrapper
from .models import City, CityLanguage, Person


def get_country_suggestions():
    return City.objects.values_list(
        'country', flat=True
    ).order_by('country').distinct()


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
            'mayor_email': AwesompleteWidgetWrapper(
                widget=forms.EmailInput,
                suggestions=(
                    'noreply@mail.com',
                    'dont_disturb@mail.com',
                    'mayor@mail.com',
                    'support@mail.com',
                ),
                min_chars=0
            )
        }


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    form = CityAdminForm
    inlines = (CityLanguageInline, CityLanguageStackedInline)
    list_display = ('name', 'country')


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
        }


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = PersonForm
    list_display = ('name', 'email')
