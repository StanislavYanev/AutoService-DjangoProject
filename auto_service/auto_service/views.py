from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required()
def home_view(request):
    return render(request, "base.html")
