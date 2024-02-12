# Change Log

## [0.6.0](https://github.com/dldevinc/django-awesomplete/tree/v0.6.0) - 2024-02-12

### Features

-   Added support for Django 5.0.
-   Added support for Python 3.12.
-   `awesomplete.js` updated to v1.1.5.

### Bug Fixes

-   Fixed https://github.com/dldevinc/django-awesomplete/issues/1.

## [0.5.2](https://github.com/dldevinc/django-awesomplete/tree/v0.5.2) - 2023-02-24

### Features

-   Test against Django 4.2.
-   Add Wagtail compatibility.

## [0.5.1](https://github.com/dldevinc/django-awesomplete/tree/v0.5.1) - 2023-01-09

### Features

-   Add Python 3.11 support (no code changes were needed, but now we test this release).

## [0.5.0](https://github.com/dldevinc/django-awesomplete/tree/v0.5.0) - 2022-08-15

### Features

-   Added support for Django 4.1.

### Bug Fixes

-   Fixed type check.

## [0.4.0](https://github.com/dldevinc/django-awesomplete/tree/v0.4.0) - 2022-05-30

### ⚠ BREAKING CHANGES

-   Dropped support for Python 3.5.

## [0.3.0](https://github.com/dldevinc/django-awesomplete/tree/v0.3.0) - 2022-01-13

-   Drop support for Python 3.4
-   Update awesomplete up to v1.1.5
-   The deprecatd `AwesompleteWidget` has been removed.
-   Allow to type a value with double quotes for `AwesompleteTagsWidgetWrapper`.

## [0.2.1](https://github.com/dldevinc/django-awesomplete/tree/v0.2.1) - 2020-10-23

-   Added `AwesompleteTagsWidgetWrapper`

## [0.2.0](https://github.com/dldevinc/django-awesomplete/tree/v0.2.0) - 2020-10-20

-   `AwesompleteWidget` is now deprecated.
-   Added `AwesompleteWidgetWrapper` that can turn any widget to Awesomplete.
-   The _minchars_ and _maxitems_ arguments was renamed to _min_chars_ and _max_items_
    respectively for new `AwesompleteWidgetWrapper`.
-   The order of arguments in lists and tuples has been reversed
    for compatibility with django choices for new `AwesompleteWidgetWrapper`.
-   Show suggestions on focus when _min_chars_ is set to zero.
-   Update dev environment
