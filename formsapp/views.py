from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm

def signup(request):
    if request.method == 'POST':
        frm = CustomUserCreationForm(request.POST)
        if frm.is_valid():
            frm.save()
            return redirect('home')   # success হলে home এ যাবে
    else:
        frm = CustomUserCreationForm()
    return render(request, 'myapp/sign_up.html', {'form': frm})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # email দিয়ে user খোঁজা
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')   # home এ redirect করবে
                else:
                    error = "Invalid password!"
                    return render(request, 'myapp/login.html', {'form': form, 'error': error})
            except User.DoesNotExist:
                error = "User not found!"
                return render(request, 'myapp/login.html', {'form': form, 'error': error})
    else:
        form = LoginForm()

    return render(request, 'myapp/login.html', {'form': form})