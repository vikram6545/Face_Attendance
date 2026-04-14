from django.urls import path
from . import views


urlpatterns = [
    # 1. Attendance lagane ka page (Selfie + Location)
    path('mark/', views.mark_attendance, name='mark_attendance'),
    
    # 2. Student ka dashboard jahan percentage dikhegi
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('signup/', views.student_signup, name='student_signup'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
]