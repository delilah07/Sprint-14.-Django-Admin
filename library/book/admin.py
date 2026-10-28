
from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_authors', 'count')
    list_display_links = ('id', 'name')

    search_fields = (
        '=id',
        'name',
        'authors__name',
        'authors__surname',
    )

    list_filter = ('authors',)
    filter_horizontal = ('authors',)
    list_per_page = 20

    fieldsets = (
        ('Static information', {
            'fields': ('name', 'description', 'authors'),
        }),
        ('Dynamic information', {
            'fields': ('count',),
        }),
    )

    @admin.display(description='Authors')
    def get_authors(self, obj):
        return ', '.join(
            f'{author.name} {author.surname}'
            for author in obj.authors.all()
        )
