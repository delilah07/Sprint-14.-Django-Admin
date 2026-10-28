
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from authentication.decorators import librarian_required

from .models import Order
from book.models import Book


@login_required(login_url='login')
def order_list(request):
    if request.user.role == 1:
        orders = Order.objects.select_related(
            'book', 'user'
        ).all()
    else:
        orders = Order.objects.select_related(
            'book', 'user'
        ).filter(user=request.user)

    return render(request, 'order/order_list.html', {
        'orders': orders,
    })


@login_required(login_url='login')
def create_order(request, book_id):
    if request.method != 'POST':
        return redirect('book_detail', book_id=book_id)

    book = get_object_or_404(Book, id=book_id)

    planned_end_at = timezone.now() + timedelta(days=14)

    order = Order.create(
        user=request.user,
        book=book,
        plated_end_at=planned_end_at,
    )

    if order is None:
        messages.error(request, 'This book is currently unavailable.')
    else:
        authors = ", ".join(
            f"{author.name} {author.surname}"
            for author in book.authors.all()
        )

        book_info = f'"{book.name}"'
        if authors:
            book_info += f" by {authors}"

        messages.success(
            request,
            f"You successfully borrowed {book_info}. "
            f"Please return it by {planned_end_at:%Y-%m-%d}."
        )

    return redirect('order_list')


@login_required(login_url='login')
@librarian_required
def return_order(request, order_id):
    if request.method != 'POST':
        return redirect('order_list')

    with transaction.atomic():
        order = Order.objects.select_for_update().select_related(
            'book'
        ).filter(pk=order_id).first()

        if order is None:
            messages.error(request, 'Order not found.')
            return redirect('order_list')

        if order.end_at is not None:
            messages.warning(request, 'This book has already been returned.')
            return redirect('order_list')

        book = Book.objects.select_for_update().get(pk=order.book_id)

        order.end_at = timezone.now()
        order.save(update_fields=['end_at'])

        book.count += 1
        book.save(update_fields=['count'])

    messages.success(request, 'Book returned successfully.')
    return redirect('order_list')

