# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .models import Login

# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         if not Login.objects.filter(username=username).exists():
#             Login.objects.create(username=username, password=password)
#             return redirect('login')
#         else:
#             return HttpResponse("User already exists")
#     return render(request, 'accounts/register.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         try:
#             user = Login.objects.get(username=username, password=password)
#             request.session['username'] = user.username
#             return redirect('home')
#         except Login.DoesNotExist:
#             return HttpResponse("Invalid credentials")
#     return render(request, 'accounts/login.html')

# def home(request):
#     username = request.session.get('username')
#     if username:
#         return HttpResponse(f"Hello {username} How are you")
#     else:
#         return redirect('login')

# def logout_view(request):
#     request.session.flush()
#     return redirect('login')
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.db import connection

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)", [username, password])
        
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM login WHERE username=%s AND password=%s", [username, password])
            user = cursor.fetchone()

        if user:
            request.session['username'] = username
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('login')

    return render(request, 'login.html')


def home_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')
    return render(request, 'home.html', {'username': username})


def logout_view(request):
    auth_logout(request)
    request.session.flush()
    return redirect('login')
