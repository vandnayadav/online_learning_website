from django.shortcuts import render, redirect
from .models import Course

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail


# ---------- NORMAL PAGES ----------
def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def courses(request):
    courses = Course.objects.all()
    return render(request, "course.html", {'course': courses})


# ---------- SIGNUP ----------
def signup_view(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        login(request, user)
        return redirect('login')

    return render(request, 'signup.html')


# ---------- LOGIN ----------
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')


# ---------- LOGOUT ----------
def logout_view(request):
    logout(request)
    return redirect('login')


# ---------- FORGOT PASSWORD ----------
def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            link = f"http://127.0.0.1:8000/reset/{uid}/{token}/"

            send_mail(
                "Password Reset",
                f"Click this link to reset password: {link}",
                "admin@example.com",
                [email],
            )

            messages.success(request, "Reset link sent to email")

        else:
            messages.error(request, "Email not found")

    return render(request, "forgot_password.html")


# ---------- RESET PASSWORD ----------
def reset_password(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)

    if request.method == "POST":
        password = request.POST['password']
        user.set_password(password)
        user.save()
        return redirect('login')

    return render(request, "reset_password.html")