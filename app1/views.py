from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import base64
from openpyxl import Workbook
from openpyxl.styles import Alignment
from django.utils.timezone import localtime
from datetime import datetime
from io import BytesIO
from django.utils.timezone import now
from django.shortcuts import render
from django.contrib import messages
from .models import Faculty, Infrastructure, Course, Catering
from django.contrib.auth import authenticate, login, logout, get_user_model

def download_feedback(request):
    # Create a new Excel workbook and worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Feedback Data"

    # Set the header row in the Excel sheet
    headers = ['Feedback Category', 'Trainee', 'Name', 'Rating', 'Description', 'Submitted At']
    ws.append(headers)

    # Set some formatting for the header row
    for cell in ws[1]:
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # Get all feedback data from the database
    feedback_data = []

    # Fetch data for each feedback category
    for model, category in [
        (Infrastructure, 'Infrastructure'),
        (Faculty, 'Faculty'),
        (Course, 'Course'),
        (Catering, 'Catering'),
    ]:
        feedback_data += [
            (category, feedback.trainee.username, feedback.infrastructure_name if model == Infrastructure else feedback.faculty_name if model == Faculty else feedback.course_name if model == Course else feedback.catering_name,
             feedback.rating, feedback.description, localtime(feedback.submitted_at).strftime("%Y-%m-%d %H:%M:%S"))
            for feedback in model.objects.all()
        ]

    # Add the data to the worksheet
    for feedback in feedback_data:
        ws.append(feedback)

    # Set the filename based on the current date and time
    file_name = f"feedback_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    
    # Set the response to download the Excel file
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    wb.save(response)

    return response

def get_filtered_feedback(model, filter_type):
    today = now().date()
    
    if filter_type == "day":
        return model.objects.filter(submitted_at__date=today).count()
    elif filter_type == "month":
        return model.objects.filter(submitted_at__year=today.year, submitted_at__month=today.month).count()
    elif filter_type == "year":
        return model.objects.filter(submitted_at__year=today.year).count()
    
    return 0

def get_feedback_data(request):
    filter_type = request.GET.get('filter', 'month')
    
    data = {
        "infrastructure": get_filtered_feedback(Infrastructure, filter_type),
        "faculty": get_filtered_feedback(Faculty, filter_type),
        "course": get_filtered_feedback(Course, filter_type),
        "catering": get_filtered_feedback(Catering, filter_type),
    }

    return JsonResponse(data)

def get_feedback_data(request):
    def get_ratings(model):
        return {i: model.objects.filter(rating=i).count() for i in range(1, 6)}

    data = {
        "infrastructure": get_ratings(Infrastructure),
        "faculty": get_ratings(Faculty),
        "course": get_ratings(Course),
        "catering": get_ratings(Catering),
    }

    return JsonResponse(data)

def generate_chart(feedbacks, title):
    rating_counts = {i: feedbacks.filter(rating=i).count() for i in range(1, 6)}

    plt.figure(figsize=(6, 4))
    plt.bar(rating_counts.keys(), rating_counts.values(), color=['red', 'orange', 'yellow', 'green', 'blue'])
    plt.xlabel('Ratings')
    plt.ylabel('Number of Feedbacks')
    plt.title(title)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return encoded_image

User = get_user_model()

def welcome_page(request):
    return render(request, "welcome.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user_firstname'] = user.first_name
                request.session['user_id'] = user.id

                if user.is_superuser:
                    return redirect('adminhome')
                else:
                    return redirect('home')

            else:
                messages.error(request, "Your account is inactive.")
                return redirect('login')
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
    if not request.user.is_staff:
        logout(request)
        request.session.flush()
        messages.success(request, "You have successfully logged out.")
    else:
        messages.success(request, "You have successfully logged out.")
    
    return redirect('login')

@login_required
def facultyfeed(request):
    if request.method == "POST":
        faculty_name = request.POST.get("faculty")
        behavior = request.POST.get("behavior")
        knowledge = request.POST.get("knowledge")
        interaction = request.POST.get("interaction")
        clarity = request.POST.get("clarity")
        response = request.POST.get("response")
        examples = request.POST.get("examples")
        motivation = request.POST.get("motivation")
        satisfaction = request.POST.get("satisfaction")
        description = request.POST.get("comments", "")

        # Validate numeric fields
        try:
            behavior = int(behavior)
            knowledge = int(knowledge)
            interaction = int(interaction)
            clarity = int(clarity)
            response = int(response)
            examples = int(examples)
            motivation = int(motivation)
            satisfaction = int(satisfaction)

            # Ensure values are within range
            for rating in [behavior, knowledge, interaction, clarity, response, examples, motivation, satisfaction]:
                if rating < 1 or rating > 5:
                    messages.error(request, "Each rating must be between 1 and 5.")
                    return redirect('facultyfeed')

        except ValueError:
            messages.error(request, "Invalid rating value. Please enter a number between 1 and 5.")
            return redirect('facultyfeed')

        # Fetch the user instance
        try:
            user_instance = User.objects.get(id=request.session.get("user_id"))
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('login')

        # Save the feedback
        Faculty.objects.create(
            trainee=user_instance,
            faculty_name=faculty_name,
            behavior=behavior,
            knowledge=knowledge,
            interaction=interaction,
            clarity=clarity,
            response=response,
            examples=examples,
            motivation=motivation,
            satisfaction=satisfaction,
            description=description
        )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('thankyou')

    return render(request, "facultyfeed.html")

@login_required
def infrafeed(request):
    if request.method == "POST":
        infrastructure_name = request.POST.get("infrastructure")
        quality = request.POST.get("quality")
        resources = request.POST.get("resources")
        maintenance = request.POST.get("maintenance")
        safety = request.POST.get("safety")
        satisfaction = request.POST.get("satisfaction")
        description = request.POST.get("comments", "")

        try:
            quality = int(quality)
            resources = int(resources)
            maintenance = int(maintenance)
            safety = int(safety)
            satisfaction = int(satisfaction)

            for rating in [quality, resources, maintenance, safety, satisfaction]:
                if rating < 1 or rating > 5:
                    messages.error(request, "Each rating must be between 1 and 5.")
                    return redirect('infrafeed')

        except ValueError:
            messages.error(request, "Invalid rating value. Please enter a number between 1 and 5.")
            return redirect('infrafeed')

        try:
            user_instance = User.objects.get(id=request.session.get("user_id"))
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('login')

        # Save the feedback
        Infrastructure.objects.create(
            trainee=user_instance,
            infrastructure_name=infrastructure_name,
            quality=quality,
            resources=resources,
            maintenance=maintenance,
            safety=safety,
            satisfaction=satisfaction,
            description=description
        )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('thankyou')

    return render(request, "infrafeed.html")

@login_required
def coursefeed(request):
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        content = request.POST.get("content")
        instructor = request.POST.get("instructor")
        materials = request.POST.get("materials")
        satisfaction = request.POST.get("satisfaction")
        description = request.POST.get("comments", "")

        try:
            content = int(content)
            instructor = int(instructor)
            materials = int(materials)
            satisfaction = int(satisfaction)

            for rating in [content, instructor, materials, satisfaction]:
                if rating < 1 or rating > 5:
                    messages.error(request, "Each rating must be between 1 and 5.")
                    return redirect('infrafeed')

        except ValueError:
            messages.error(request, "Invalid rating value. Please enter a number between 1 and 5.")
            return redirect('infrafeed')

        try:
            user_instance = User.objects.get(id=request.session.get("user_id"))
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('login')

        # Save the feedback
        Course.objects.create(
            trainee=user_instance,
            course_name=course_name,
            content=content,
            instructor=instructor,
            materials=materials,
            satisfaction=satisfaction,
            description=description
        )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('thankyou')

    return render(request, "coursefeed.html")

@login_required
def cateringfeed(request):
    if request.method == "POST":
        catering_name = request.POST.get("catering_name")
        food_quality = request.POST.get("food_quality")
        service_quality = request.POST.get("service_quality")
        Cleanliness = request.POST.get("Cleanliness")
        Affordable = request.POST.get("Affordable")
        overall_satisfaction = request.POST.get("overall_satisfaction")
        description = request.POST.get("comments", "")

        try:
            food_quality = int(food_quality)
            service_quality = int(service_quality)
            Cleanliness = int(Cleanliness)
            Affordable = int(Affordable)
            overall_satisfaction = int(overall_satisfaction)

            for rating in [food_quality, service_quality, Cleanliness, Affordable, overall_satisfaction]:
                if rating < 1 or rating > 5:
                    messages.error(request, "Each rating must be between 1 and 5.")
                    return redirect('infrafeed')

        except ValueError:
            messages.error(request, "Invalid rating value. Please enter a number between 1 and 5.")
            return redirect('infrafeed')

        try:
            user_instance = User.objects.get(id=request.session.get("user_id"))
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('login')

        # Save the feedback
        Catering.objects.create(
            trainee=user_instance,
            catering_name=catering_name,
            food_quality=food_quality,
            service_quality=service_quality,
            Cleanliness=Cleanliness,
            Affordable=Affordable,
            overall_satisfaction=overall_satisfaction,
            description=description
        )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('thankyou')

    return render(request, "cateringfeed.html")

def contact(request):
    return render(request, "contact.html")

def admin_home(request):
    return render(request, 'adminhome.html')

def thankyou(request):
    return render(request, "thankyou.html")

def serve_meta(request):
    return JsonResponse({
        "status": "ok",
        "message": "This is a placeholder meta.json file"
    })