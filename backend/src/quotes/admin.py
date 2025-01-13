from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.safestring import SafeString
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter

from contrib.admin_mixins import GUIDAdminMixin
from quotes.models import Author, Category, Quote


@admin.register(Author)
class AuthorAdmin(GUIDAdminMixin, ModelAdmin):
    def has_module_permission(self, request: HttpRequest) -> bool:
        return False

    list_display = ('name', 'created', 'modified')
    list_filter = ('name', ('created', RangeDateFilter), ('modified', RangeDateFilter))
    readonly_fields = ('created', 'modified')
    search_fields = ordering = ('name',)
    fieldsets = (
        (
            _('Author'), {'fields': ('name',)}
        ),
    )


@admin.register(Category)
class CategoryAdmin(GUIDAdminMixin, ModelAdmin):
    def has_module_permission(self, request: HttpRequest) -> bool:
        return False

    list_display = ('name', 'created', 'modified')
    list_filter = ('name', ('created', RangeDateFilter), ('modified', RangeDateFilter))
    readonly_fields = ('created', 'modified')
    search_fields = ordering = ('name',)
    fieldsets = (
        (
            _('Category'), {'fields': ('name',)}
        ),
    )


@admin.register(Quote)
class QuoteAdmin(GUIDAdminMixin, ModelAdmin):
    autocomplete_fields = ('author', 'category')
    list_display = ('author', 'quote_text_short', 'ratio', 'created', 'modified')
    list_filter = ('author', ('created', RangeDateFilter), ('modified', RangeDateFilter))
    readonly_fields = ('created', 'modified', 'quote_hash')
    search_fields = ordering = ('likes', 'dislikes')
    fieldsets = (
        (
            _('Quote'), {'classes': ('tab',), 'fields': ('category', 'author', 'quote_text')}
        ),
        (
            _('Metadata'),
            {'classes': ('tab',),
             'fields': ('quote_hash', ('image_url', 'image_alt_text', 'origin'), ('likes', 'dislikes'))}
        ),
    )

    def quote_text_short(self, obj: Quote) -> str:
        return _(f'"{obj.quote_text[:24]}{"..." if len(obj.quote_text) > 24 else ""}"').__str__()

    quote_text_short.short_description = _('quote')

    def ratio(self, obj: Quote) -> SafeString:
        total_votes: int = obj.likes + obj.dislikes

        if total_votes == 0:
            like_percentage: int = 50  # Default to 50% each if no votes yet
            dislike_percentage: int = 50
        else:
            like_percentage: int = (obj.likes / total_votes) * 100
            dislike_percentage: int = (obj.dislikes / total_votes) * 100

        return format_html(
            '''
<div class="mb-4 flex h-4 overflow-hidden rounded bg-gray-100 text-xs">
    <div style="width: {}%" class="bg-green-500 transition-all duration-500 ease-out"></div>
    <div style="width: {}%" class="bg-red-500 transition-all duration-500 ease-out"></div>
</div>
<div class="mb-2 flex items-center justify-between text-xs space-x-4">
    <div class="text-gray-600 ">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
             class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M6.633 10.25c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V2.75a.75.75 0 0 1 .75-.75 2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282m0 0h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H13.48c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23H5.904m10.598-9.75H14.25M5.904 18.5c.083.205.173.405.27.602.197.4-.078.898-.523.898h-.908c-.889 0-1.713-.518-1.972-1.368a12 12 0 0 1-.521-3.507c0-1.553.295-3.036.831-4.398C3.387 9.953 4.167 9.5 5 9.5h1.053c.472 0 .745.556.5.96a8.958 8.958 0 0 0-1.302 4.665c0 1.194.232 2.333.654 3.375Z" />
        </svg> {}
    </div>
    <div class="text-gray-600">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
             class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M7.498 15.25H4.372c-1.026 0-1.945-.694-2.054-1.715a12.137 12.137 0 0 1-.068-1.285c0-2.848.992-5.464 2.649-7.521C5.287 4.247 5.886 4 6.504 4h4.016a4.5 4.5 0 0 1 1.423.23l3.114 1.04a4.5 4.5 0 0 0 1.423.23h1.294M7.498 15.25c.618 0 .991.724.725 1.282A7.471 7.471 0 0 0 7.5 19.75 2.25 2.25 0 0 0 9.75 22a.75.75 0 0 0 .75-.75v-.633c0-.573.11-1.14.322-1.672.304-.76.93-1.33 1.653-1.715a9.04 9.04 0 0 0 2.86-2.4c.498-.634 1.226-1.08 2.032-1.08h.384m-10.253 1.5H9.7m8.075-9.75c.01.05.027.1.05.148.593 1.2.925 2.55.925 3.977 0 1.487-.36 2.89-.999 4.125m.023-8.25c-.076-.365.183-.75.575-.75h.908c.889 0 1.713.518 1.972 1.368.339 1.11.521 2.287.521 3.507 0 1.553-.295 3.036-.831 4.398-.306.774-1.086 1.227-1.918 1.227h-1.053c-.472 0-.745-.556-.5-.96a8.95 8.95 0 0 0 .303-.54" />
        </svg> {}
    </div>
</div>
            ''',
            like_percentage, dislike_percentage, obj.likes, obj.dislikes
        )

    ratio.short_description = _('Like/Dislike ratio')
