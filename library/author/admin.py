
from django.contrib import admin
from .models import Author
from book.models import Book

class BookFilter(admin.SimpleListFilter):
    title = 'books'
    parameter_name = 'books'

    def lookups(self, request, model_admin):
        books = Book.objects.order_by('name')
        return [
            (str(book.pk), book.name)
            for book in books
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(books__pk=self.value()).distinct()
        return queryset
    
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

    list_filter = (BookFilter,)
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


