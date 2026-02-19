from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    name = 'attendance'

def ready(self):
    import attendance.signals  # Signals ko ready hone par import karna hota hai
