import django
from django.contrib import admin

if django.VERSION >= (2, 0):
    from django.urls import re_path, include
else:
    from django.conf.urls import url as re_path, include


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'', include('app.urls')),
]
