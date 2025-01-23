from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.models import User

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

def facultyfeed(request):
    return render(request, "facultyfeed.html")

def infrafeed(request):
    return render(request, "infrafeed.html")

def coursefeed(request):
    return render(request, "coursefeed.html")

def cateringfeed(request):
    return render(request, "cateringfeed.html")

from django.http import JsonResponse

def serve_meta(request):
    return JsonResponse({
        "status": "ok",
        "message": "This is a placeholder meta.json file"
    })