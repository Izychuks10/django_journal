from django.shortcuts import render, redirect, get_object_or_404
from .models import Journal, Blog, Comment
from .forms import BlogForm, JournalForm, UserRegistrationForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TeamMember
from datetime import datetime



def index(request):
    return render(request, 'index.html')

def journals(request):
    journals = Journal.objects.all()
    return render(request, 'journals.html', {'journals': journals})

def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'blog.html', {'blogs': blogs})

def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog')  # Redirect to the blog page after saving
    else:
        form = BlogForm()
    return render(request, 'add_blog.html', {'form': form})

def add_journal(request):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('journals')  # Redirect to the journals page after saving
    else:
        form = JournalForm()
    return render(request, 'add_journal.html', {'form': form})

def about(request):
    team_members = TeamMember.objects.all()  # Retrieve all team members from the database
    return render(request, 'about.html', {'team_members': team_members})

def contact(request):
    return render(request, 'contact.html')


def admin(request):
    return render(request, 'admin.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Ensure the user account is active
            user.is_staff = True
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            return redirect('login')  # Ensure this matches the name in your urls.py
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required  # Ensure only logged-in users can comment
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # If the user is not authenticated, store the blog ID and redirect to login
    if not request.user.is_authenticated:
        request.session['last_visited_blog'] = blog.id
        return redirect('login')  # Redirect to login page

    comments = blog.comments.all()  # Get all comments related to the blog post

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('blog_detail', blog_id=blog.id)  # Redirect to the same page after submission
    else:
        form = CommentForm()

    # Clear the session variable after using it
    if 'last_visited_blog' in request.session:
        del request.session['last_visited_blog']

    return render(request, 'blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'form': form,
        'current_year': datetime.now().year
    })

def your_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()  # Create an empty form instance
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    # Fetch journals or any other data you want to display
    journals = Journal.objects.all()  # Assuming you have a Journal model
    return render(request, 'home.html', {'journals': journals})

def your_logout_view(request):
    logout(request)  # Log the user out
    return redirect('index')

def your_home_view(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Check if there's a last visited blog post
            last_visited_blog = request.session.get('last_visited_blog')
            if last_visited_blog:
                # Redirect to the blog detail page
                return redirect('blog_detail', blog_id=last_visited_blog)
            else:
                return redirect('home')  # Redirect to home or another page after login
    # Render login form
    return render(request, 'login.html')


@login_required  # Ensure only logged-in users can delete comments
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user is the owner of the comment
    if request.user == comment.user:
        comment.delete()  # Delete the comment
    return redirect('blog_detail', blog_id=comment.blog.id)
