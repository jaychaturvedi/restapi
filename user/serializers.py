from rest_framework import serializers
from django.contrib.auth import  get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = User
        fields = ['username','password'] #  'email','city','contact','address',,'role'
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)