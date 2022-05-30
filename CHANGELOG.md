# Change Log

## [0.4.0](https://github.com/dldevinc/django-awesomplete/tree/v0.4.0) - 2022-05-30
### ⚠ BREAKING CHANGES
- Dropped support for Python 3.5.

## [0.3.0](https://github.com/dldevinc/django-awesomplete/tree/v0.3.0) - 2022-01-13
- Drop support for Python 3.4
- Update awesomplete up to v1.1.5
- The deprecatd `AwesompleteWidget` has been removed.
- Allow to type a value with double quotes for `AwesompleteTagsWidgetWrapper`.

## [0.2.1](https://github.com/dldevinc/django-awesomplete/tree/v0.2.1) - 2020-10-23
- Added `AwesompleteTagsWidgetWrapper`

## [0.2.0](https://github.com/dldevinc/django-awesomplete/tree/v0.2.0) - 2020-10-20
- `AwesompleteWidget` is now deprecated.
- Added `AwesompleteWidgetWrapper` that can turn any widget to Awesomplete.
- The *minchars* and *maxitems* arguments was renamed to *min_chars* and *max_items*
respectively for new `AwesompleteWidgetWrapper`.
- The order of arguments in lists and tuples has been reversed 
for compatibility with django choices for new `AwesompleteWidgetWrapper`.
- Show suggestions on focus when *min_chars* is set to zero.
- Update dev environment
