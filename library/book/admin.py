
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Book
from author.models import Author

from django import forms

class AuthorChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name} {obj.surname}'.strip()


class AuthorMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name} {obj.surname}'.strip()
    
class BookAdminForm(forms.ModelForm):
    authors = AuthorMultipleChoiceField(
        queryset=Author.objects.all().order_by('name', 'surname'),
        required=False,
        label='Authors',
        widget=FilteredSelectMultiple(
            'Authors',
            is_stacked=False,
        ),
    )

    class Meta:
        model = Book
        fields = ('name', 'description', 'authors', 'count')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['authors'].initial = self.instance.authors.all()

    def save(self, commit=True):
        book = super().save(commit=commit)

        if commit:
            self.save_m2m()

        return book

    def save_m2m(self):
        if self.instance.pk:
            self.instance.authors.set(self.cleaned_data['authors'])


class BookIdFilter(admin.SimpleListFilter):
    title = 'book ID'
    parameter_name = 'book_id'

    def lookups(self, request, model_admin):
        return [
            (str(book_id), str(book_id))
            for book_id in Book.objects.order_by('id')
            .values_list('id', flat=True)
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id=self.value())
        return queryset


class BookTitleFilter(admin.SimpleListFilter):
    title = 'book title'
    parameter_name = 'book_title'

    def lookups(self, request, model_admin):
        return [
            (title, title)
            for title in Book.objects.order_by('name')
            .values_list('name', flat=True)
            .distinct()
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name=self.value())
        return queryset


class BookAuthorFilter(admin.SimpleListFilter):
    title = 'author'
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        authors = Author.objects.filter(
            books__isnull=False
        ).distinct().order_by('name', 'surname')

        return [
            (
                str(author.pk),
                f'{author.name} {author.surname}'.strip(),
            )
            for author in authors
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(authors__pk=self.value())
        return queryset


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm

    list_display = ('id', 'name', 'get_authors', 'count')
    list_display_links = ('id', 'name')

    search_fields = (
        '=id',
        'name',
        'authors__name',
        'authors__surname',
    )

    list_filter = (
        BookIdFilter,
        BookTitleFilter,
        BookAuthorFilter,
    )

    list_per_page = 20

    fieldsets = (
        ('Book information', {
            'fields': ('name', 'description', 'authors'),
        }),
        ('Inventory information', {
            'fields': ('count',),
        }),
    )

    @admin.display(description='Authors')
    def get_authors(self, obj):
        return ', '.join(
            f'{author.name} {author.surname}'.strip()
            for author in obj.authors.all()
        )

    def change_view(
        self, request, object_id, form_url='', extra_context=None
    ):
        extra_context = extra_context or {}
        book = self.get_object(request, object_id)

        if book:
            extra_context['title'] = f'Change book: {book.name}'

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )
