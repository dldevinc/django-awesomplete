from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class Article(models.Model):
    title = models.CharField(
        max_length=255
    )
    author = models.CharField(
        max_length=255,
        blank=True,
        help_text="Suggestions are loaded from already populated instances"
    )
    tags = TaggableManager(
        blank=True,
        help_text="Suggestions are loaded from existing Tag instances"
    )
    publish_at = models.DateField(
        _("publish at"),
        null=True,
        blank=True,
        help_text="Custom suggestions"
    )

    class Meta:
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.title
