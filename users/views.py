from django.shortcuts import render,redirect,get_list_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Create your views here.

def index(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        login(request,user)
        return redirect('users:dashboard')
    else:
        return render(request, 'users/login.html')


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            form = UserCreationForm()
            messages.success(request, "User has been Created!")
        else:
            messages.error(request, "Failed to create the User! Something went wrong!")    
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context=context)
    

@login_required
def dashboard(request):
    user = request.user
    if user.is_superuser == True:
        context = {
            'title': "Admin::Dashboard"
        }
        return render(request, 'users/admin/dashboard.html', context=context)
    else:
        context = {
            'username': user.username,
            'title': "User::Dashboard"
        }
        return render(request, 'users/user/dashboard.html', context=context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('users:home')


@login_required
def user_delete(request, pkid):
    user = User.objects.get(id=pkid).delete()
    messages.success(request,  ' Deleted!')
    return redirect("users:dashboard")

@login_required    
def users_view(request):
    user = get_list_or_404(User)
    context =  {
        'users': user,
    }
    return render(request, 'users/admin/users_page.html', context=context)

@login_required
def user_detail_view(request, pkid):
    user = User.objects.get(id=pkid)
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'last_login': user.last_login,
        'date_joined': user.date_joined,
    }
    return render(request, 'users/admin/detail_view.html', context=context)


def user_update_view(request, pkid):
    user = User.objects.get(id=pkid)
    form = UserChangeForm(instance=user)
    if request.method == "POST":
        form = UserChangeForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "User data has been updated!!")
        else:
            form = UserChangeForm(instance=user)
            messages.error(request, "Something went wrong!!!")
    context = {
        'form': form
    }
    return render(request, 'users/admin/user_change_page.html', context)