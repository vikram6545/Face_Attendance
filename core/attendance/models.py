from django.db import models
from django.contrib.auth.models import User

# 1. Semester (e.g., Sem 1, Sem 2)
class Semester(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name

# 2. Subject
class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    def __str__(self): return f"{self.name} ({self.semester.name})"

# 3. Timetable (Schedule)
class Schedule(models.Model):
    DAYS = [(0,'Mon'), (1,'Tue'), (2,'Wed'), (3,'Thu'), (4,'Fri'), (5,'Sat')]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

# 4. Student Profile (Photo & Location)
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.IntegerField(unique=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    face_baseline = models.ImageField(upload_to='profiles/') # Ye photo match ke liye hogi
    class_lat = models.FloatField(default=22.747275) # indore default Lat
    class_lon = models.FloatField(default=75.895755) # indore default Lon

# 5. Holiday (Chuttiyan)
class Holiday(models.Model):
    date = models.DateField(unique=True)
    reason = models.CharField(max_length=100)

# 6. Attendance Table
class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

class StudentQuery(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    email = models.EmailField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False) # Admin ise check kar sakta hai

    def __str__(self):
        return f"Query by {self.name} - {self.roll_no}"    
