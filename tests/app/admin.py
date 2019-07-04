from django import forms
from django.contrib import admin
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
    inlines = (CityLanguageInline, )
    list_display = ('name', 'country')
