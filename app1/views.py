from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Faculty, User, Infrastructure, Course
from django.contrib.auth import get_user_model
User = get_user_model()
def welcome_page(request):
    return render(request, "welcome.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user securely
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                # Set session data
                request.session['user_firstname'] = user.first_name
                request.session['user_id'] = user.id
                messages.success(request, "You have successfully logged in!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login')
        except User.DoesNotExist:
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
        
        if not all([firstname, email, username, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect('signup')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('signup')
        
        user = User.objects.create_user(
            first_name=firstname,
            email=email,
            username=username,
            password=password
        )
        user.is_active = True
        user.save()
        messages.success(request, "Signup successful! You can now log in.")
        return redirect('login')

    return render(request, "signup.html")

@login_required
def home_page(request):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must log in to access the home page.")
        return redirect('login')

    firstname = request.session.get('user_firstname', '')
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
        user_id = request.session.get("user_id")
        print(f"User ID from session: {user_id}")  # Debugging statement
        try:
            user_instance = User.objects.get(id=user_id)
            print(f"User instance retrieved: {user_instance}")  # Debugging statement
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

        # Fetch the user instance
        user_id = request.session.get("user_id")  # Ensure this session is set correctly when the user logs in
        try:
            instance = User.objects.get(id=user_id)  # Fetch the user instance directly using .get()
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('login')

        # Create a new Course record
        Course.objects.create(
            Trainee=instance,  # Assign the User instance to the ForeignKey field
            course_name=course_name,
            rating=rating,
            description=description
        )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('thankyou')

    return render(request, "coursefeed.html")

def cateringfeed(request):
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