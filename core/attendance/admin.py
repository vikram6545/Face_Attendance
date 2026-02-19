from django.contrib import admin
from .models import Semester, Subject, Schedule, StudentProfile, Holiday, Attendance, StudentQuery

admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Schedule)
admin.site.register(StudentProfile)
admin.site.register(Holiday)
admin.site.register(Attendance)

@admin.register(StudentQuery)
class StudentQueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no', 'email', 'reason', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'roll_no', 'email', 'reason')
