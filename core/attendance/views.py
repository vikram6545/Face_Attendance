import base64
import math
import os
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import StudentSignupForm
from datetime import timedelta,date
from .forms import QueryForm



# Models aur utils
from .models import StudentProfile, Attendance, Schedule, Holiday, Subject
from .utils import verify_face 

def get_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

@login_required
def mark_attendance(request):
    if request.method == 'GET':
        return render(request, 'attendance/mark.html')

    if request.method == 'POST':
        user = request.user
        profile = user.studentprofile
        today = datetime.now()
        if Holiday.objects.filter(date=today.date()).exists():
            messages.error(request, "Tday is a holiday: " + Holiday.objects.get(date=today.date()).reason)
            return redirect('student_dashboard')
        
        # --- DEBUGGING START ---
        print("---------- DEBUGGING SCHEDULE ----------")
        print(f"Current Day (Python): {today.weekday()}") # 0=Mon, 5=Sat
        print(f"Current Time (Python): {today.time()}")
        print(f"Student Semester: {profile.semester}")
        
        # Check karein ki kya is Semester ke subjects hain bhi?
        all_subs = Subject.objects.filter(semester=profile.semester)
        print(f"Subjects in this Semester: {[s.name for s in all_subs]}")

        # Check karein ki total Schedule mein kitni entries hain
        total_sched = Schedule.objects.count()
        print(f"Total Schedules in DB: {total_sched}")
        print("----------------------------------------")
        # --- DEBUGGING END ---

        # 1. Schedule Check
        sched = Schedule.objects.filter(
            subject__semester=profile.semester,
            day=today.weekday(),
            start_time__lte=today.time(),
            end_time__gte=today.time()
        ).first()
        

        if not sched:
            # Agar class ka time nahi hai ya schedule galat hai
            messages.warning(request, f'Attendance Fail: Abhi aapki koi class scheduled nahi hai (Day: {today.strftime("%A")}, Time: {today.strftime("%H:%M")}).')
            return redirect('student_dashboard')
        
        current_subject = sched.subject

        # 2. Duplicate Check
        if Attendance.objects.filter(student=user, subject=current_subject, date=today.date()).exists():
            messages.info(request, f'Dubaara koshish: Aapne {current_subject.name} ki attendance aaj pehle hi laga di hai.')
            return redirect('student_dashboard')

        try:
            # 3. Location Check
            u_lat = float(request.POST.get('lat', 0))
            u_lon = float(request.POST.get('lon', 0))
            dist = get_distance(u_lat, u_lon, profile.class_lat, profile.class_lon)
            
            if dist > 100:
                messages.error(request, f'Location Fail: Aap class se {int(dist)}m door hain. Kripya class ke andar jayein.')
                return render(request, 'attendance/mark.html')

            # 4. Image/Camera Check
            img_data = request.POST.get('image')
            if not img_data:
                messages.error(request, 'Camera Error: Photo capture nahi ho payi. Dobara try karein.')
                return render(request, 'attendance/mark.html')

            # Image processing logic (Same as before)
            format, imgstr = img_data.split(';base64,')
            temp_path = os.path.join(settings.MEDIA_ROOT, f'temp_capture_{user.id}.jpg')
            with open(temp_path, 'wb') as f:
                f.write(base64.b64decode(imgstr))

            # 5. Face Matching (Strict Check)
            match_result = verify_face(profile.face_baseline.path, temp_path)
            
            if os.path.exists(temp_path):
                os.remove(temp_path)

            if match_result is True:
                Attendance.objects.create(student=user, subject=current_subject, status=True)
                messages.success(request, f'Success: {current_subject.name} ki attendance lag gayi hai!')
                return redirect('student_dashboard')
            else:
                # Jab face match na ho ya andhera ho
                messages.error(request, 'Face Match Fail: Chehra sahi se pehchana nahi gaya. Kripya roshni mein khade ho kar dobara try karein.')
                return render(request, 'attendance/mark.html')

        except Exception as e:
            messages.error(request, f'System Error: {str(e)}')
            return render(request, 'attendance/mark.html')
@login_required
def student_dashboard(request):
    user = request.user
    profile = user.studentprofile
    subjects = Subject.objects.filter(semester=profile.semester)
    joining_date = user.date_joined.date()
    today = date.today()
    all_holidays = set(Holiday.objects.filter(date__range=[joining_date, today]).values_list('date', flat=True))
    attendance_data = []
    
    for sub in subjects:
        total_marked = 0
        scheduled_days = list(Schedule.objects.filter(subject=sub).values_list('day', flat=True))
        current_date = joining_date
        while current_date <= today:
            print(f"Checking {sub.name} for {current_date}, Day: {current_date.weekday()}")
            if current_date.weekday() in scheduled_days:
                if current_date.weekday() != 6 and current_date not in all_holidays:  # Sunday aur holidays ko skip karein
                    total_marked += 1
            current_date += timedelta(days=1)
        user_attended = Attendance.objects.filter(student=user, subject=sub, status=True).count()
        percentage = (user_attended / total_marked * 100) if total_marked > 0 else 0
            
        attendance_data.append({
            'subject': sub.name,
            'total': total_marked,
            'attended': user_attended,
            'percentage': round(percentage, 2),
            'short': percentage < 75
        })
        # Context mein profile bhi bhej rahe hain
    context = {
        'attendance_data': attendance_data,
        'profile': profile,
        'user': user,
        'joining_date': joining_date
    }
    if request.method == 'POST' and 'submit_query' in request.POST:
        query_form = QueryForm(request.POST)
        if query_form.is_valid():
            query = query_form.save(commit=False)
            query.student = request.user
            query.save()
            messages.success(request, "Aapki query admin ko bhej di gayi hai!")
            return redirect('student_dashboard')
    else:
        query_form = QueryForm(initial={
            'name': request.user.username,
            'email': request.user.email,
            'roll_no': request.user.studentprofile.roll_no # Agar profile mein hai
        })

    # Context mein query_form add karein
    context['query_form'] = query_form
    return render(request, 'attendance/dashboard.html', context)

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create Profile
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = StudentSignupForm()

    return render(request, 'attendance/signup.html', {'form': form})

