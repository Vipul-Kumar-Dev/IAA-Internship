from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import Faculty, Infrastructure, Course, Catering
from django.contrib.auth import get_user_model

User = get_user_model()

def welcome_page(request):
    return render(request, "welcome.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
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

    return render(request, "login.html")

@login_required
def home_page(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must log in to access the home page.")
        return redirect('login')

    firstname = request.session.get('user_firstname', '')
    return render(request, "home.html", {"firstname": firstname})

def logout_view(request):
    request.session.flush()
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

@login_required
def facultyfeed(request):
    if request.method == "POST":
        trainee = request.user
        faculty_name = request.POST.get("faculty")
        rating = request.POST.get("rating")
        description = request.POST.get("comments", "")

        print(f"Trainee: {trainee.username}, Faculty: {faculty_name}, Rating: {rating}, Comments: {description}")

        if not trainee:
            return HttpResponse("User not logged in.", status=400)
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return HttpResponse("Rating must be between 1 and 5.", status=400)
        except ValueError:
            return HttpResponse("Invalid rating value.", status=400)

        Faculty.objects.create(
            trainee=trainee,
            faculty_name=faculty_name,
            rating=rating,
            description=description
        )

        return redirect('thankyou')

    return render(request, "facultyfeed.html")

@login_required
def infrafeed(request):
    if request.method == "POST":
        infrastructure_name = request.POST.get("infrastructure")
        rating = request.POST.get("rating")
        description = request.POST.get("comments", "")

        if not all([infrastructure_name, rating]):
            messages.error(request, "Infrastructure name and rating are required.")
            return redirect('infrafeed')

        user_instance = request.user
        Infrastructure.objects.create(
            Trainee=user_instance,
            infrastructure_name=infrastructure_name,
            rating=int(rating),
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

        if not all([course_name, rating]):
            messages.error(request, "Course name and rating are required.")
            return redirect('coursefeed')

        user_instance = request.user
        Course.objects.create(
            Trainee=user_instance,
            course_name=course_name,
            rating=int(rating),
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

        if not all([catering_name, rating]):
            messages.error(request, "Catering name and rating are required.")
            return redirect('cateringfeed')

        user_instance = request.user
        Catering.objects.create(
            Trainee=user_instance,
            catering_name=catering_name,
            rating=int(rating),
            description=description,
        )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('thankyou')

    return render(request, "cateringfeed.html")

def contact(request):
    return render(request, "contact.html")

def thankyou(request):
    return render(request, "thankyou.html")

def serve_meta(request):
    return JsonResponse({
        "status": "ok",
        "message": "This is a placeholder meta.json file"
    })