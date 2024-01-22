from django.contrib import admin
from .models import *

admin.site.register(Shift)
admin.site.register(Employee)
admin.site.register(Schedule)
admin.site.register(Attendance)
admin.site.register(LeaveRequest)
admin.site.register(LeaveApproval)
admin.site.register(EmergencyContact)