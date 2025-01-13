import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class GUIDModelMixin(models.Model):
    """
    Mixin that adds a guid (Globally Unique IDentifier) field to a model
    """
    guid = models.UUIDField(_('GUID'), default=uuid.uuid4, unique=True)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    """
    Mixin that adds a 'created' and 'updated' field to a model
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ResponsibleUserMixin(models.Model):
    """
    Mixin that adds a 'created' and 'updated' field to a model
    """
    user_created = models.ForeignKey(
        to=AbstractBaseUser, null=True, on_delete=models.SET_NULL, related_name='%(class)s_created')
    user_modified = models.ForeignKey(
        to=AbstractBaseUser, null=True, on_delete=models.SET_NULL, related_name='%(class)s_modified')

    class Meta:
        abstract = True
