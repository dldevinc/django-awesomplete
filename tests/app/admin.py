from django import forms
from django.contrib import admin
from suggestions.widgets import SuggestionsWidget
from .models import City


def get_country_suggestions():
    return City.objects.values_list(
        'country', flat=True
    ).order_by('country').distinct()


class CityAdminForm(forms.ModelForm):
    class Meta:
        model = City
        fields = forms.ALL_FIELDS
        widgets = {
            'country': SuggestionsWidget(
                suggestions=get_country_suggestions
            )
        }


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    form = CityAdminForm
    list_display = ('name', 'country')
