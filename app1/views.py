from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Faculty, User, Infrastructure, Course, Catering
from django.contrib.auth import authenticate, login

def welcome_page(request):
    return render(request, "welcome.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_firstname'] = user.first_name
            request.session['user_id'] = user.id
            request.session.save()
            messages.success(request, "You have successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate input
        if not all([firstname, email, username, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect('signup')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
        # Check for existing email or username
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('signup')
        
        # Save new user with hashed password
        user = User.objects.create_user(
            first_name=firstname,
            email=email,
            username=username,
            password=password  # No need to hash; create_user handles it
        )
        user.is_active = True  # Ensure the user is active
        user.save()
        messages.success(request, "Signup successful! You can now log in.")
        return redirect('login')

    return render(request, "login.html")
@login_required
def home_page(request):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must log in to access the home page.")
        return redirect('login')

    firstname = request.user.first_name
    return render(request, "home.html", {"firstname": firstname})

def logout_view(request):
    # Clear user session
    request.session.flush()
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

@login_required
def facultyfeed(request):
    if request.method == "POST":
        faculty_name = request.POST.get("faculty")
        rating = request.POST.get("rating")
        description = request.POST.get("comments", "")

        # Validate input
        if not all([faculty_name, rating]):
            messages.error(request, "Faculty name and rating are required.")
            return redirect('facultyfeed')

        # Get the logged-in user from session
        try:
            user_instance = User.objects.get(id=request.session.get("user_id"))
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('login')

        # Create feedback
        Faculty.objects.create(
            Trainee=user_instance,
            faculty_name=faculty_name,
            rating=rating,
            description=description
        )
        messages.success(request, "Feedback submitted successfully!")
        return redirect('thankyou')

    return render(request, "facultyfeed.html")

@login_required
def infrafeed(request):
    if request.method == "POST":
        infrastructure_name = request.POST.get("infrastructure")
        rating = request.POST.get("rating")
        description = request.POST.get("comments", "")

        # Validate input
        if not all([infrastructure_name, rating]):
            messages.error(request, "Infrastructure name and rating are required.")
            return redirect('infrafeed')

        try:
            user_instance = User.objects.get(id=request.session.get("user_id"))
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('login')

        Infrastructure.objects.create(
            Trainee=user_instance,
            infrastructure_name=infrastructure_name,
            rating=rating,
            description=description
        )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('thankyou')

    return render(request, "infrafeed.html")

@login_required
def coursefeed(request):
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        rating = request.POST.get("rating")
        description = request.POST.get("comments", "")

        # Validate input
        if not all([course_name, rating]):
            messages.error(request, "Course name and rating are required.")
            return redirect('coursefeed')

        try:
            user_instance = User.objects.get(id=request.session.get("user_id"))
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('login')

        Course.objects.create(
            Trainee=user_instance,
            course_name=course_name,
            rating=rating,
            description=description
        )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('thankyou')
    return render(request, "coursefeed.html")

@login_required
def cateringfeed(request):
    if request.method == "POST":
        catering_name = request.POST.get("catering_name")
        rating = request.POST.get("rating")
        description = request.POST.get("comments", "")

        # Validate input
        if not all([catering_name, rating]):
            messages.error(request, "Catering name and rating are required.")
            return redirect('cateringfeed')

        try:
            user_instance = User.objects.get(id=request.session.get("user_id"))
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('login')

        Catering.objects.create(
            Trainee=user_instance,
            catering_name=catering_name,
            rating=rating,
            description=description
        )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('thankyou')
    return render(request, "cateringfeed.html")

def contact(request):
    return render(request, "contact.html")

def thankyou(request):
    return render(request, "thankyou.html")

from django.http import HttpResponse, JsonResponse

def serve_meta(request):
    return JsonResponse({
        "status": "ok",
        "message": "This is a placeholder meta.json file"
    })