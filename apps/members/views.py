from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

def login_usuarios(request):
    if request.method=='GET':
        return render(request, 'members/login.html', {}) 
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else: # redirect to error page
            messages.success(request, ('Usted tiene un error en su usuario o contraseña'))
            return redirect('members:login_usuarios')

@login_required
def logout_view(request):
    logout(request)
    return redirect("members:login_usuarios")


