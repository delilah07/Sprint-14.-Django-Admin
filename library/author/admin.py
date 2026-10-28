
from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'surname',
        'patronymic',
    )

    search_fields = (
        'name',
        'surname',
        'patronymic',
    )

    list_per_page = 20

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.books.exists():
            return False

        return super().has_delete_permission(request, obj)
