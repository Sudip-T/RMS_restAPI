from django.db import models
from authentication.models import CustomUser
from django.core.exceptions import ValidationError


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    birth_date = models.DateField()
    date_joined = models.DateField()
    emergency_contact = models.ForeignKey(
        'EmergencyContact', on_delete=models.SET_NULL, blank=True, null=True, related_name='emergency_contacts')
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class EmergencyContact(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='emergency_contacts')
    emg_contct_name = models.CharField(max_length=50)
    emg_contct_phone = models.CharField(max_length=15)
    emg_contct_address = models.TextField()

    def __str__(self):
        return self.emg_contct_name
    


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    clock_in = models.TimeField()
    clock_out = models.TimeField(blank=True, null=True)
    attendance_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee.id} - {self.employee.first_name}'
    

class Shift(models.Model):
    start_time = models.CharField(max_length=5)
    end_time = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.start_time}-{self.end_time}'



class Schedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT)
    date = models.DateField()

    def __str__(self):
        return f'{self.employee.id} - {self.employee.first_name}'
    


class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_reason = models.TextField()
    leave_status = models.CharField(default='Pending')
    leave_status_note = models.TextField(blank=True, null=True)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee.id} - {self.employee.first_name}'
    
    # def clean(self):
    #     if self.start_date and self.end_date and self.start_date > self.end_date:
    #         raise ValidationError('start date must be before or eqaul to end date')
        
    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super().save(*args,**kwargs)


class LeaveApproval(models.Model):
    leave_request = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    leave_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    approval_date = models.DateTimeField(auto_now_add=True)
    leave_status_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.leave_request.employee.id} - {self.leave_request.employee.first_name}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.leave_request.leave_status = self.leave_status
        self.leave_request.leave_status_note = self.leave_status_note
        self.leave_request.save()