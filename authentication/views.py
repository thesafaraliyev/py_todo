from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib import messages


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('auth:login')

    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})


