
from django.shortcuts import render, get_object_or_404
from .models import Book


def book_list(request):
    books = Book.objects.all()

    title = request.GET.get('title', '').strip()
    author = request.GET.get('author', '').strip()

    if title:
        books = books.filter(name__icontains=title)

    if author:
        books = books.filter(
            authors__name__icontains=author
        ) | books.filter(
            authors__surname__icontains=author
        )

    books = books.distinct()

    return render(request, 'book/book_list.html', {
        'books': books,
        'title_query': title,
        'author_query': author,
    })


def book_detail(request, book_id):
    selected_book = get_object_or_404(Book, id=book_id)

    return render(request, 'book/book_detail.html', {
        'selected_book': selected_book
    })
