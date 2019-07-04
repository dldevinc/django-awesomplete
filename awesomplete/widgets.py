import copy
from django import forms
from django.conf import settings
from django.forms import widgets
from django.forms.fields import CallableChoiceIterator


class AwesompleteWidget(widgets.TextInput):
    template_name = 'awesomplete/widget.html'

    def __init__(self, attrs=None, suggestions=(), minchars=1, maxitems=10, autofirst=True):
        super().__init__(attrs)
        self.minchars = minchars
        self.maxitems = maxitems
        self.autofirst = autofirst
        self.suggestions = suggestions

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.attrs = self.attrs.copy()
        obj.suggestions = copy.deepcopy(self.suggestions, memo)
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

    def get_datalist_id(self, name):
        id_ = self.attrs.get('datalist')
        if id_ is None:
            id_ = name + '_datalist'
        return id_

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs.setdefault('class', '')
        attrs.update({
            'data-sort': 'false',
            'data-minchars': self.minchars,
            'data-maxitems': self.maxitems,
            'data-autofirst': self.autofirst,
            'class': attrs['class'] + (' ' if attrs['class'] else '') + 'admin-awesomplete',
        })
        return attrs

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        datalist_id = self.get_datalist_id(name)
        final_attrs = context['widget']['attrs']
        final_attrs['list'] = datalist_id

        context['widget'].update({
            'datalist': datalist_id,
            'suggestions': list(self.suggestions)
        })
        return context

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        return forms.Media(
            js=(
                'awesomplete/js/vendor/awesomplete%s.js' % extra,
                'awesomplete/js/widget.js',
            ),
            css={
                'screen': (
                    'awesomplete/css/awesomplete.css',
                ),
            },
        )
