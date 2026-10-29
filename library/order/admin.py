
from django import forms
from django.contrib import admin

from .models import Order
from book.models import Book
from authentication.models import CustomUser


class BookChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        full_name = ' '.join(
            part for part in (obj.first_name, obj.last_name)
            if part
        )
        return f'{full_name} ({obj.email})' if full_name else obj.email

class OrderAdminForm(forms.ModelForm):
    book = BookChoiceField(
        queryset=Book.objects.all().order_by('name'),
        label='Book',
    )
    user = UserChoiceField(
        queryset=CustomUser.objects.all().order_by('email'),
        label='User',
    )

    class Meta:
        model = Order
        fields = '__all__'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm

    list_display = (
        'id',
        'get_book',
        'get_user',
        'created_at',
        'plated_end_at',
        'end_at',
        'is_returned',
    )

    list_display_links = ('id', 'get_book')
    readonly_fields = ('book_display', 'user_display', 'created_at')

    fieldsets = (
        ('Order information', {
            'fields': ('book_display', 'user_display'),
        }),
        ('Issue and return dates', {
            'fields': ('created_at', 'plated_end_at', 'end_at'),
        }),
    )

    list_filter = ('created_at', 'plated_end_at', 'end_at')
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

    @admin.display(description='Book', ordering='book__name')
    def get_book(self, obj):
        return self.book_display(obj)

    @admin.display(description='Book')
    def book_display(self, obj):
        if not obj or not obj.book:
            return '-'

        title = obj.book.name
        authors = ', '.join(
            f'{author.name} {author.surname}'.strip()
            for author in obj.book.authors.all()
        )

        return f'{title} — {authors}' if authors else title

    @admin.display(description='User', ordering='user__email')
    def get_user(self, obj):
        return self.user_display(obj)

    @admin.display(description='User')
    def user_display(self, obj):
        if not obj or not obj.user:
            return '-'

        full_name = ' '.join(
            part for part in (
                obj.user.first_name,
                obj.user.last_name,
            ) if part
        )

        return (
            f'{full_name} ({obj.user.email})'
            if full_name
            else obj.user.email
        )

    @admin.display(boolean=True, description='Returned')
    def is_returned(self, obj):
        return obj.end_at is not None
