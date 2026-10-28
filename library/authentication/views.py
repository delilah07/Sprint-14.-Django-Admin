
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied

from .models import CustomUser
from .decorators import librarian_required



def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        middle_name = request.POST.get('middle_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        role = request.POST.get('role', '0')

        errors = []

        if not first_name or not last_name or not email or not password:
            errors.append('Please fill in all required fields.')

        if len(first_name) > 20 or len(last_name) > 20:
            errors.append('First and last names must not exceed 20 characters.')

        if len(middle_name) > 20:
            errors.append('Middle name must not exceed 20 characters.')

        if len(email) > 100 or '@' not in email:
            errors.append('Please enter a valid email address.')

        if password != password_confirm:
            errors.append('Passwords do not match.')

        if len(password) < 8:
            errors.append('Password must contain at least 8 characters.')

        if role not in ('0', '1'):
            errors.append('Please select a valid role.')

        if CustomUser.objects.filter(email__iexact=email).exists():
            errors.append('A user with this email already exists.')

        if errors:
            return render(request, 'authentication/register.html', {
                'errors': errors,
                'form_data': request.POST,
            })

        CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            role=int(role),
        )

        return redirect('login')

    return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'authentication/login.html', {
            'error': 'Invalid email or password.'
        })

    return render(request, 'authentication/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

    return redirect('home')

@librarian_required
def user_list_view(request):
    users = CustomUser.objects.all().order_by('last_name', 'first_name')

    return render(request, 'authentication/user_list.html', {
        'users': users,
    })

@librarian_required
def user_detail_view(request, user_id):
    selected_user = get_object_or_404(CustomUser, id=user_id)

    return render(request, 'authentication/user_detail.html', {
        'selected_user': selected_user,
    })