from.models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','password']
        # extra_kwargs = {
        #     'password':{'write_only':True}
        # }

    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     groups_data = validated_data.pop('groups', [])  # Extract groups data

    #     instance = self.Meta.model(**validated_data)

    #     if password is not None:
    #         instance.set_password(password)

    #     instance.save()

    #     # Now handle groups separately
    #     instance.groups.set(groups_data)

    #     return instance

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)   #this hashes the password 
        instance.save()
        return instance
        
    # def create(self, validated_data):
    #     user = CustomUser.objects.create(email=validated_data['email'])
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user