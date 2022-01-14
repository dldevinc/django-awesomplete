import copy
from collections.abc import Iterable

from django import forms
from django.conf import settings
from django.forms import widgets
from django.forms.fields import CallableChoiceIterator


def build_suggestions(suggestions):
    """
    Returns a list of { label, value } pairs for their subsequent JSON serialization.

    :rtype: list[(str, str)]
    """
    choices = []
    for suggestion in suggestions:
        if isinstance(suggestion, str):
            choices.append((suggestion, suggestion))
        elif isinstance(suggestion, dict):
            choices.append((
                suggestion.get("label", ""),
                suggestion.get("value", "")
            ))
        elif isinstance(suggestion, Iterable):
            value, label = suggestion[:2]
            choices.append((label, value))
        else:
            raise TypeError(suggestion)
    return choices


class AwesompleteWidgetWrapper(widgets.Widget):
    """
    This class is a wrapper to a given widget to add suggestions.
    """
    css_class = "admin-awesomplete"
    template_name = "awesomplete/widget_wrapper.html"

    def __init__(
        self,
        widget=None,
        suggestions=(),
        min_chars=1,
        max_items=10,
        autofirst=True
    ):
        if widget is None:
            widget = widgets.TextInput
        if isinstance(widget, type):
            widget = widget()
        self.widget = widget

        self.attrs = self.widget.attrs
        self.suggestions = suggestions
        self.min_chars = min_chars
        self.max_items = max_items
        self.autofirst = autofirst

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.widget = copy.deepcopy(self.widget, memo)
        obj.attrs = self.widget.attrs
        memo[id(self)] = obj
        return obj

    def _get_suggestions(self):
        return self._suggestions

    def _set_suggestions(self, value):
        if isinstance(value, CallableChoiceIterator):
            self._suggestions = value
        elif callable(value):
            self._suggestions = CallableChoiceIterator(value)
        else:
            self._suggestions = list(value)

    suggestions = property(_get_suggestions, _set_suggestions)

    @property
    def is_hidden(self):
        return self.widget.is_hidden

    @property
    def media(self):
        media = widgets.Media()
        media = media + self.widget.media

        extra = "" if settings.DEBUG else ".min"
        media = media + forms.Media(
            js=(
                "awesomplete/js/vendor/awesomplete%s.js" % extra,
                "awesomplete/js/widget.js",
            ),
            css={
                "screen": (
                    "awesomplete/css/awesomplete.css",
                ),
            },
        )
        return media

    @staticmethod
    def get_list_id(name, attrs):
        id_ = attrs.get("list_id")
        if id_ is None:
            id_ = attrs.get("id", name) + "_list"
        return id_

    def get_context(self, name, value, attrs, renderer=None):
        extra_attrs = {
            "data-minchars": self.min_chars,
            "data-maxitems": self.max_items,
            "data-autofirst": self.autofirst,
        }
        attrs = self.build_attrs(extra_attrs, attrs)
        attrs = self.build_attrs(self.attrs, attrs)

        # add CSS-class
        attrs["class"] = attrs.get("class", "") + " " + self.css_class

        # set list ID
        list_id = self.get_list_id(name, attrs)
        attrs["data-list"] = "#%s" % list_id

        context = {
            "rendered_widget": self.widget.render(name, value, attrs, renderer),
            "is_hidden": self.is_hidden,
            "name": name,
            "list_id": list_id,
            "suggestions": build_suggestions(self.suggestions)
        }
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs, renderer)
        return self._render(self.template_name, context, renderer)

    def value_from_datadict(self, data, files, name):
        return self.widget.value_from_datadict(data, files, name)

    def value_omitted_from_data(self, data, files, name):
        return self.widget.value_omitted_from_data(data, files, name)

    def id_for_label(self, id_):
        return self.widget.id_for_label(id_)


class AwesompleteTagsWidgetWrapper(AwesompleteWidgetWrapper):
    css_class = "admin-awesomplete-tags"
