
from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'surname',
        'patronymic',
        'get_books',
    )

    search_fields = (
        'id',
        'name',
        'surname',
        'patronymic',
        'books__name',
    )

    list_filter = ('books',)
    list_per_page = 20

    fieldsets = (
        ('Author information', {
            'fields': ('name', 'surname', 'patronymic'),
        }),
        ('Books', {
            'fields': ('books',),
        }),
    )

    @admin.display(description='Books')
    def get_books(self, obj):
        return ', '.join(book.name for book in obj.books.all())

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.books.exists():
            return False

        return super().has_delete_permission(request, obj)
