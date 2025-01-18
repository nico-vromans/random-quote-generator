from hashlib import sha256

from django.db import models
from django.utils.translation import gettext_lazy as _

from contrib.models import GUIDModelMixin, TimestampMixin
from quotes.api.registry import API_CLIENTS


class Author(GUIDModelMixin, TimestampMixin, models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Category(GUIDModelMixin, TimestampMixin, models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class QuoteOrigin(GUIDModelMixin, TimestampMixin, models.Model):
    url = models.URLField(null=True)
    api_client_key = models.CharField(max_length=255, null=True,
                                      choices=[(client, client.replace('_', ' ').title()) for client in API_CLIENTS])

    class Meta:
        verbose_name = _('Origin')
        verbose_name_plural = _('Origins')
        ordering = ('url',)

    def __str__(self) -> str:
        return self.url


class Quote(GUIDModelMixin, TimestampMixin, models.Model):
    author = models.ForeignKey(to=Author, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, blank=True)
    quote_text = models.TextField(unique=True)
    quote_hash = models.CharField(max_length=64, unique=True, editable=False)
    image_url = models.URLField(null=True)
    image_alt_text = models.CharField(max_length=255, null=True)
    origin = models.ForeignKey(to=QuoteOrigin, on_delete=models.SET_NULL, null=True, blank=True)
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = _('Quote')
        verbose_name_plural = _('Quotes')
        ordering = ('category', '-likes')
        unique_together = ('author', 'quote_text')

    def __str__(self) -> str:
        author: str = _(f' by {self.author.name}' if self.author else ' (Unknown Author)')
        category: str = _(f' ({self.category.name})' if self.category else ' (No Category)')

        return _(f'"{self.quote_text[:24]}{"..." if len(self.quote_text) > 24 else ""}"{author}{category}').__str__()

    def save(self, *args, **kwargs) -> None:
        if not self.quote_hash or not self.pk or self.quote_has_changed():
            self.quote_hash = sha256(self.quote_text.encode('utf-8')).hexdigest()

        super().save(*args, **kwargs)

    def quote_has_changed(self) -> bool:
        """
        Check if the quote has changed.

        :returns: boolean that indicates if the quote has changed.
        :rtype: bool
        """
        if not self.pk:
            return True

        original: Quote = Quote.objects.filter(pk=self.pk).first()

        return original and original.quote_text != self.quote_text
