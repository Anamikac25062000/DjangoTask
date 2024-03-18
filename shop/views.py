from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .models import Product


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            # Store successful login count in cookies
            successful_logins = request.COOKIES.get('successful_logins', 0)
            response = redirect('product_list')
            response.set_cookie('successful_logins', int(successful_logins) + 1)
            # Reset failed login attempts
            if 'login_attempts' in request.session:
                del request.session['login_attempts']
            return response
        else:
            messages.error(request, 'Invalid username or password.')
            # Increment failed login attempts stored in session
            request.session['login_attempts'] = request.session.get('login_attempts', 0) + 1
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('login')

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
