from.models import CustomUser
from rest_framework import serializers
from django.contrib.auth import password_validation


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8,max_length=16, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','password']
        # extra_kwargs = {
        #     'password':{'write_only':True}
        # }


    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)   #this hashes the password 
        instance.save()
        return instance



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True, required=True)

    class Meta:
        fields = ['old_password', 'new_password', 'confirm_password']

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('old password do not match')
        return value
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'password_error':"new password and confirm password do not match"})
        password_validation.validate_password(data['new_password'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user