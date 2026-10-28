
from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'book',
        'user',
        'created_at',
        'plated_end_at',
        'end_at',
        'is_returned',
    )

    list_display_links = ('id', 'book')

    list_filter = (
        'created_at',
        'plated_end_at',
        'end_at',
    )

    search_fields = (
        '=id',
        'book__name',
        'user__email',
        'user__first_name',
        'user__last_name',
    )

    date_hierarchy = 'created_at'
    list_select_related = ('book', 'user')
    list_per_page = 20

    @admin.display(boolean=True, description='Returned')
    def is_returned(self, obj):
        return obj.end_at is not None

    readonly_fields = ('created_at',)
