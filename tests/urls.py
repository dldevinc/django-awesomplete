import django
from django.contrib import admin

if django.VERSION >= (2, 0):
    from django.urls import include, re_path
else:
    from django.conf.urls import include
    from django.conf.urls import url as re_path


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'', include('app.urls')),
]
