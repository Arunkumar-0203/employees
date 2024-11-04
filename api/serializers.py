# employees/serializers.py
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from api.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'password', 'department', 'role']
        extra_kwargs = {'password': {'write_only': True}}  # Hide password in responses

    def validate_email(self, value):
        """
        Validate email to ensure it's unique on creation and not duplicated on update.
        """
        # Check if updating or creating
        if self.instance:  # Update operation
            if Employee.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("An employee with this email already exists.")
        else:  # Create operation
            if Employee.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Hash the password if it's being updated
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
