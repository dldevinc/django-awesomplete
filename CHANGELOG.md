# Change Log

## [0.2.0](https://github.com/dldevinc/django-awesomplete/tree/v0.2.0) - 2020-10-20
- `AwesompleteWidget` is now deprecated.
- Added `AwesompleteWidgetWrapper` that can turn any widget to Awesomplete.
- The *minchars* and *maxitems* arguments was renamed to *min_chars* and *max_items*
respectively for new `AwesompleteWidgetWrapper`.
- The order of arguments in lists and tuples has been reversed 
for compatibility with django choices for new `AwesompleteWidgetWrapper`.
- Show suggestions on focus when *min_chars* is set to zero.
- Update dev environment
