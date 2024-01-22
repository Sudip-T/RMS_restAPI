from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'shift', ShiftView, basename='shift')
router.register(r'schedule', ScheduleView, basename='schedule')
router.register(r'employee', EmployeeView, basename='employee')
router.register(r'attendance', AttendanceView, basename='attendance')
router.register(r'leave-request', LeaveRequestView, basename='leave-request')
router.register(r'leave-approval', LeaveApprovalView, basename='leave-approval')
router.register(r'emergency-contact', EmergencyContactView, basename='emergency-contact')


urlpatterns = router.urls