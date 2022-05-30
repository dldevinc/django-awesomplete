import datetime
from django import forms
from django.contrib import admin
from django.utils.timezone import now, timedelta
from taggit.forms import TagWidget
from taggit.models import Tag

from awesomplete.widgets import AwesompleteTagsWidgetWrapper, AwesompleteWidgetWrapper

from .models import Article


def get_author_suggestions():
    return Article.objects.values_list(
        "author",
        flat=True
    ).order_by("author").distinct()


def get_tag_suggestions():
    return Tag.objects.values_list(
        "name",
        flat=True
    ).order_by("name").distinct()


def next_weekday(weekday=0):
    """
    :param weekday: 0 = Monday, 1=Tuesday, 2=Wednesday, ...
    """
    days_ahead = weekday - now().weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return now() + datetime.timedelta(days_ahead)


def date_generator():
    yield now(), "Today"
    yield now() + timedelta(days=1), "Tomorrow"
    yield next_weekday(), "Next monday"


def date_formatter(dates):
    for date, label in dates:
        yield (
            date.date().strftime("%Y-%m-%d"),
            label
        )


def get_date_suggestions():
    """
    Example with chained generators
    """
    for date, label in date_formatter(date_generator()):
        yield {
            "label": label,
            "value": date
        }


class ArticleAdminForm(forms.ModelForm):
    publish_at = forms.DateTimeField(
        required=False,
        label="Publish at",
        widget=AwesompleteWidgetWrapper(
            suggestions=get_date_suggestions,
            min_chars=0
        )
    )

    class Meta:
        model = Article
        fields = forms.ALL_FIELDS
        widgets = {
            "author": AwesompleteWidgetWrapper(
                suggestions=get_author_suggestions,
                min_chars=0
            ),
            "tags": AwesompleteTagsWidgetWrapper(
                widget=TagWidget,
                suggestions=get_tag_suggestions
            ),
        }


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    fieldsets = [
        (None, {
            "fields": ["title"]
        }),
        ("Awesomplete", {
            "fields": ["author", "tags", "publish_at"]
        }),
    ]
    list_display = ("title", "author", "publish_at")
