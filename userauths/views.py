from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages, auth
from core import *
from django.conf import settings
from userauths.models import User



# Create your views here.

#User = settings.AUTH_USER_MODEL

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Hey {username}, You account was created successfully')
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            
            login(request, new_user)
            return redirect("core:home")     
    else:
        print("User can't register")
        form = UserRegisterForm()
    
    
    context = {
        'form': form,
    }
    return render(request, 'userauths/sign-up.html', context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"you are already logged in")
        return redirect("core:home")
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
        
            if user is not None:
               login(request, user)
               messages.success(request, "You are logged in.")
               return redirect("core:home")
            else:
               messages.warning(request, "user Does not Exist, Create a new account.")
        except:
            messages.warning(request, f"User with {email} does not exist")
            
    return render(request, 'userauths/sign-in.html')

def logout_view(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('userauths:sign-in')