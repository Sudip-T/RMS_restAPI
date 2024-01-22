from .models import * 
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, SAFE_METHODS



class EmployeeView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Employee.objects.all()
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetEmployeeSerializers
        return EmployeeSerializers
    

class EmergencyContactView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    pagination_class = PageNumberPagination


class ShiftView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = ShiftSerializers
    queryset = Shift.objects.all()
    pagination_class = PageNumberPagination


class ScheduleView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()


class AttendanceView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()


class LeaveRequestView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = LeaveRequest.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetLeaveRequestSerializer
        return LeaveRequestSerializer


class LeaveApprovalView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = LeaveApprovalSerializer
    queryset = LeaveApproval.objects.all()