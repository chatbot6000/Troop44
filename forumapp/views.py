from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    #put in something to see if the user is already logged in
    if "user" in request.session:
        context ={
            'user':User.objects.get(id=request.session['user'])
        }     
        return render(request, 'index.html', context)
    # return redirect('/posts')
    return render(request, 'index.html')

def events(request):
    #put in something to see if the user is already logged in
    if "user" in request.session:
        context ={
            'user':User.objects.get(id=request.session['user'])
        }     
        return render(request, 'events.html', context)
    # return redirect('/posts')
    return render(request, 'events.html')

def location(request):
    #put in something to see if the user is already logged in
    if "user" in request.session:
        context ={
            'user':User.objects.get(id=request.session['user'])
        }     
        return render(request, 'location.html', context)
    # return redirect('/posts')
    return render(request, 'location.html')

def about(request):
    #put in something to see if the user is already logged in
    if "user" in request.session:
        userid = request.session["user"]
        context ={
            'user':User.objects.get(id=userid)
        }     
        return render(request, 'about.html', context)
    # return redirect('/posts')
    return render(request, 'about.html')

def gallery(request):
    #put in something to see if the user is already logged in
    if "user" in request.session:
        context ={
            'user':User.objects.get(id=request.session['user'])
        }     
        return render(request, 'gallery.html', context)
    # return redirect('/posts')
    return render(request, 'gallery.html')

def login(request):
    
    return render(request, 'login.html')

def register(request):
    
    return render(request, 'register.html')

def register_action(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:

            hashedpw =bcrypt.hashpw(request.POST['pword'].encode(), bcrypt.gensalt()).decode()
            newUser = User.objects.create(
                first_name=request.POST['fname'],
                last_name=request.POST['lname'],
                email=request.POST['email'],
                password=hashedpw,
            )
            request.session['user'] = newUser.id
            return redirect('/')
    else:
        return redirect("/")

def login_action(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
        else:
            LoggedUser = User.objects.get(email=request.POST['email'])
            request.session['user'] = LoggedUser.id
            return redirect('/')
    else:
        return redirect('/')

def logout(request):
    #request.session.clear()
    #request.session.flush()
    #request.session = {}
    try:
        del request.session['user']
    except KeyError:
        pass
    return redirect('/')

def posts(request):
    userid = request.session["user"]
    context ={
        'allposts':Post.objects.all(),
        'user':User.objects.get(id=userid)
    }
    return render(request, 'posts.html', context)

def update(request, userid):
    loggedin_userid = request.session["user"]
    context={
        'username':User.objects.get(id=loggedin_userid)
    }
    return render(request,"myaccount.html",context)  

def process_update(request, userid):
    loggedin_userid = request.session["user"]
    if request.method == 'POST':
        errors = User.objects.update_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/update/{loggedin_userid}')
        else:
            user=User.objects.get(id=userid)        
            user.firstname=request.POST['fname']
            user.lastname=request.POST['lname']
            user.email=request.POST['email']
            user.save()
            fname = request.POST['fname']
            
            return redirect(f'/update/{loggedin_userid}')
    else:
        return redirect('/') 

def view_user(request, userid):
    loggedin_userid = request.session["user"]
    context ={
        'allposts':Post.objects.filter(user__id=userid),
        'username':User.objects.get(id=userid),
        'userid':User.objects.get(id=loggedin_userid)
    }
    return render(request, 'user.html', context)  

def addlike(request, post_id):
    user = User.objects.get(id=request.session['user'])
    post = Post.objects.get(id=post_id)
    user.likes.add(post)
    return redirect('/posts')  

def addpost(request):
    user = User.objects.get(id=request.session['user'])
    if request.method == 'POST':
        errors = Post.objects.post_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/posts')
        else:
            newquote = Post.objects.create(
                text = request.POST['text'],
                user = user,
            )
            return redirect('/posts')
    else:
        return redirect('/')
    
def delete(request, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect('/posts')

