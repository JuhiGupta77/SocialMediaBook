from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post
from django.contrib.auth.decorators import login_required


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # go to your own page i.e. index page
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')


# Create your views here.
@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # assigning new user details to Profile object
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('account_settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        messages.info(request, 'You are Not SignedUp !')
        return render(request, 'signup.html')


@login_required(login_url='signin')
def upload(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    print("upload:", upload)
    return render(request, 'index.html', {'user_profile': user_profile})


@login_required(login_url='signin')
def account_settings(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
        print("user_profile:", user_profile)
    except:
        return redirect('signin')

    if request.method == 'POST':
        # as was defined input type="file" name="image" in account_settings.html page for image tag
        # similarly are the bio and location tags
        if request.FILES.get('image') is None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') is not None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('account_settings')
    return render(request, 'account_settings.html', {'user_profile': user_profile})


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')