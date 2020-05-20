from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login,authenticate
# Create your views here.

@csrf_protect
def login(request):
    if request.method != 'GET':
        try:
            print('request - ',request)
            username = request.POST['username']
            password = request.POST['password']
            print(username,password)
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user is not None:
                # print("User Login:  Username:" + username + '    Password:' + password)
                auth.login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('/')
            else:
                messages.info(request, 'Username or Password wrong!')
                return redirect('/', {'message': 'Username or Password wrong!'})
        except:
            return render(request, "404.html")

        return render(request, 'accounts/login.html')
    else:
        if request.user.is_active:
            if request.user.is_authenticated:
                return redirect('/')
    return render(request, 'accounts/login.html')

@csrf_protect
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            print(password1)
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                print("Username Taken")
                return render(request, '/accounts/register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                print("Email Taken")
                return render(request, '/accounts/register.html')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name, last_name=last_name)
                user.save();
                users = [user]
                print(users)
                print('user created')
                auth.login(request, user)
                return redirect("/", {'users': users})
        else:
            messages.info(request, 'password not matching..')
            print('password not matching..')
            return render(request, 'accounts/register.html')
    else:
        print('request.method != POST')
        return render(request, 'accounts/register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')