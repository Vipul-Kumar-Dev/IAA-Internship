"""
URL configuration for TrainingFeedbackSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.generic import RedirectView
from app1 import views as v1
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v1.welcome_page),
    path('Login_Page/', v1.login_page, name='login'),
    path('signup/', v1.signup, name='signup'),
    path('home/', v1.home_page, name='home'),
    path('logout/', v1.logout_view, name='logout'),
    path('Faculty_Feed/', v1.facultyfeed, name='facultyfeed'),
    path('Infrastructure_Feed/', v1.infrafeed, name='infrafeed'),
    path('Course_Feed/', v1.coursefeed, name='coursefeed'),
    path('Catering_Feed/', v1.cateringfeed, name='cateringfeed'),
    path('meta.json', v1.serve_meta, name='meta_json'),
    path('Contact', v1.contact, name='contact'),
    path('ThankYou', v1.thankyou, name='thankyou'),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico', permanent=True)),
    path('adminhome/', v1.admin_home, name='adminhome'),
    path('download_faculty_feedback/', v1.download_faculty_feedback, name='download_faculty_feedback'),
    path('download_infrastructure_feedback/', v1.download_infrastructure_feedback, name='download_infrastructure_feedback'),
    path('download_course_feedback/', v1.download_course_feedback, name='download_course_feedback'),
    path('download_catering_feedback/', v1.download_catering_feedback, name='download_catering_feedback'),
]
