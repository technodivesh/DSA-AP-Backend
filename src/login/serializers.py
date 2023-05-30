from rest_framework import serializers
from .models import t_Employee

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_Employee
        fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }