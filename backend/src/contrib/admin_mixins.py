from collections import OrderedDict
from typing import Sequence

from django.contrib import admin
from django.http import HttpRequest


class OrderedSet(OrderedDict):
    def __init__(self, *args) -> None:
        super().__init__()

        if args:
            iterable: any = args[0]

            if isinstance(iterable, (list, tuple)):
                for item in iterable:
                    self.add(item)
            elif isinstance(iterable, dict):
                super().update(iterable)
            else:
                raise TypeError('Unsupported data type for OrderedSet')

    def add(self, item: any) -> None:
        self[item] = None

    def update(self, __m: any, **kwargs) -> None:
        if isinstance(__m, (list, tuple)):
            for item in __m:
                self.add(item)
        elif isinstance(__m, dict):
            super().update(__m)
        else:
            raise TypeError('Unsupported data type for update')

    def remove(self, item: any) -> None:
        if item in self:
            del self[item]
        else:
            raise KeyError(f'Item {item} not found in OrderedSet')


class BaseAdminMixin(admin.ModelAdmin):
    mixin_readonly_fields = ()
    mixin_fields = ()

    @classmethod
    def get_mixin_readonly_fields(cls) -> tuple:
        fields = OrderedSet()

        for base in reversed(cls.__bases__):
            if issubclass(base, BaseAdminMixin) and base != BaseAdminMixin:
                fields.update(base.get_mixin_readonly_fields())

        fields.update(cls.mixin_readonly_fields)

        return tuple(fields)

    @classmethod
    def get_mixin_fields(cls) -> tuple:
        fields = OrderedSet()

        for base in cls.__bases__:
            if issubclass(base, BaseAdminMixin) and base != BaseAdminMixin:
                fields.update(base.get_mixin_fields())

        fields.update(cls.mixin_fields)

        return tuple(fields)

    def get_readonly_fields(self, request, obj=None) -> tuple:
        """
        Automatically add the read-only fields from the Mixin subclasses in order of class inheritance declaration and
        add any other read-only fields from those subclasses later.
        """
        original_readonly: tuple = super().get_readonly_fields(request, obj)
        mixin_readonly: tuple = self.get_mixin_readonly_fields()

        return mixin_readonly + tuple(f for f in original_readonly if f not in mixin_readonly)

    def get_fieldsets(self, request: HttpRequest, obj=None) -> tuple:
        """
        Same as ``get_readonly_fields()``, but for the normal fieldsets.
        """
        fieldsets: list[tuple[None, dict[str, list[any] | any]]] | any = super().get_fieldsets(request, obj)
        mixin_fields: tuple = self.get_mixin_fields()

        if not fieldsets:
            all_fields: Sequence[str | Sequence[str]] = self.get_fields(request, obj)
            fieldsets = ((None, {'fields': all_fields}),)
        else:
            first_fieldset_fields = OrderedSet()

            # Add mixin fields first
            for field in mixin_fields:
                first_fieldset_fields.add(field)

            # Add existing/normal fields next
            for field in fieldsets[0][1]['fields']:
                if field not in first_fieldset_fields:
                    first_fieldset_fields.add(field)

            fieldsets[0][1]['fields'] = tuple(first_fieldset_fields)

        return fieldsets

    def get_list_display(self, request: HttpRequest) -> tuple:
        """
        Same as ``get_readonly_fields()`` and ``get_fieldsets()``, but for the list display.
        """
        original_list_display: tuple[str] = super().get_list_display(request=request)
        mixin_fields: tuple = self.get_mixin_fields()

        if isinstance(original_list_display, (tuple, list)):
            return mixin_fields + tuple(f for f in original_list_display if f not in mixin_fields)
        else:
            return original_list_display


class GUIDAdminMixin(BaseAdminMixin):
    mixin_readonly_fields = ('guid',)
    mixin_fields = ('guid',)


class TimeStampAdminMixin(BaseAdminMixin):
    mixin_readonly_fields = (
        'created',
        'modified',
    )
    mixin_fields = (
        'created',
        'modified',
    )
