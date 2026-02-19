from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import StudentProfile
@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)
        send_mail(
            subject='Welcome to Attendance System',
            message=f'Hello {instance.username}, your student profile has been created successfully for the attendance system.',
            from_email='admin@attendance.com',
            recipient_list=[instance.email],)


    