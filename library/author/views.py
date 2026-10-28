
from django.shortcuts import render, redirect, get_object_or_404
from .models import Author
from authentication.decorators import librarian_required


@librarian_required
def author_list(request):
    authors = Author.get_all()
    error = None
    success = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            name = request.POST.get('name', '').strip()
            surname = request.POST.get('surname', '').strip()
            patronymic = request.POST.get('patronymic', '').strip()

            if not name or not surname:
                error = 'Name and surname are required.'
            else:
                Author.objects.create(
                    name=name,
                    surname=surname,
                    patronymic=patronymic
                )
                return redirect('author_list')

        elif action == 'delete':
            author_id = request.POST.get('author_id')
            author = get_object_or_404(Author, id=author_id)

            if author.books.exists():
                error = (
                    f'Cannot delete {author.name} {author.surname}: '
                    'this author is associated with books.'
                )
            else:
                author.delete()
                return redirect('author_list')

    authors = Author.get_all()

    return render(
        request,
        'author/author_list.html',
        {
            'authors': authors,
            'error': error,
            'success': success,
        }
    )
