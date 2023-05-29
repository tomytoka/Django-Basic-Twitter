from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Profile, Post
from .forms import PostForm, SignUpForm,ProfilePicForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

def home(request):
    posts = Post.objects.all().order_by("-created_at")
    if request.user.is_authenticated:
        form = PostForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, ("Posted!"))
                return redirect('home')
		
		
        return render(request, 'home.html', {"posts":posts, "form":form})
    else:
        return render(request, 'home.html', {"posts":posts})


def profile_list(request):
    if request.user.is_authenticated: 
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html',{"profiles":profiles})
    else:
        messages.success(request,("You must be logged."))
        return redirect('home')
    
def profile(request,pk):
    if request.user.is_authenticated: 
        profile = Profile.objects.get(user_id=pk)
        posts=Post.objects.filter(user_id=pk)
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow" :
                current_user_profile.follows.remove(profile)
            else :
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, 'profile.html',{"profile":profile,"posts":posts})
    else:
        messages.success(request,("You must be logged."))
        return redirect('home')

def login_user(request):
    if request.method =="POST":
        username= request.POST['username']
        password= request.POST['password']
        user= authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("Welcome back {user.username}"))
            return redirect('home')
        else:
            messages.success(request,("Error login in , please try again."))
            return redirect('login')

    else:
        return render(request, 'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("You have logged out."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #first_name = form.cleaned_data['first_name']
            #last_name = form.cleaned_data['last_name']
            #email = form.cleaned_data['email']

            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You have succesfully Register!"))
            return redirect('home')
            

    return render(request, 'register.html', {'form':form })


def update_user(request):
    if request.user.is_authenticated:
        current_user= User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form =  ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request,current_user)
            messages.success(request,("Profile Updated."))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form,'profile_form':profile_form})
        
    else:
        messages.success(request,("You must be logged in to view this page"))
        return render(request, 'home', {})