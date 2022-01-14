import django

from .views import IndexView

if django.VERSION >= (2, 0):
    from django.urls import re_path
else:
    from django.conf.urls import url as re_path


app_name = "app"
urlpatterns = [
    re_path(r'', IndexView.as_view()),
]
