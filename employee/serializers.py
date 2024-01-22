from rest_framework import serializers
from .models import *



class GetEmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'



class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['user','id']

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = 'admin@!123'
        user = CustomUser.objects.create(email=email, first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()

        validated_data['user'] = user

        return super().create(validated_data)
    
    def update(self, instance,validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        user = instance.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        instance = super().update(instance, validated_data)
        return instance
    

# todo : link multiple emergency_contact object to particular employee object
class EmergencyContactSerializer(serializers.ModelSerializer):
    # employee = EmployeeSerializers()
    class Meta:
        model = EmergencyContact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method in ['GET', 'LIST']:
            self.fields['employee'] = EmployeeSerializers()


    def create(self, validated_data):
        emp_id = validated_data.get('employee')
        employee_obj = Employee.objects.get(id=emp_id.id)

        emergency_contact_obj = EmergencyContact.objects.create(**validated_data)

        employee_obj.emergency_contact = emergency_contact_obj
        employee_obj.save()

        return emergency_contact_obj
    


class ShiftSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method in ['GET', 'LIST']:
            self.fields['employee'] = EmployeeSerializers()
            self.fields['shift'] = ShiftSerializers()


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method in ['GET', 'LIST']:
            self.fields['employee'] = EmployeeSerializers()



class GetLeaveRequestSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializers()
    class Meta:
        model = LeaveRequest
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.context['request'].method in ['GET', 'LIST']:
    #         self.fields['employee'] = EmployeeSerializers()


    def create(self, validated_data):
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        employee = validated_data.get('employee')
        instance = LeaveRequest.objects.filter(employee=employee.id)
        if len(instance) >= 2:
            raise serializers.ValidationError('You can request only 2 leaves at a time')
        # todo : limit queryset as employee might have huge amount of leave request associated
        # todo : try to customize error message
        for i in instance:
            if start_date == i.start_date:
                raise serializers.ValidationError('You have already requested leave on this date')
        if start_date > end_date:
            raise serializers.ValidationError('start date must be before or equal to end date')
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        employee = validated_data.get('employee')
        leave_instance = LeaveRequest.objects.filter(employee=employee.id)
        # todo : limit queryset as employee might have huge amount of leave request associated
        # todo : try to customize error message
        for i in leave_instance:
            if start_date == i.start_date:
                raise serializers.ValidationError('You have already requested leave on this date')
        if start_date > end_date:
            raise serializers.ValidationError('start date must be before or equal to end date')
        
        return super().update(instance, validated_data)
    


class LeaveApprovalSerializer(serializers.ModelSerializer):
    # leave_request = LeaveRequestSerializer()
    class Meta:
        model = LeaveApproval
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method in ['GET', 'LIST']:
            self.fields['leave_request'] = LeaveRequestSerializer()