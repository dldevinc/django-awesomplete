from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    tags = TaggableManager(blank=True)
    publish_at = models.DateField(_("publish at"), null=True, blank=True)

    class Meta:
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.title
