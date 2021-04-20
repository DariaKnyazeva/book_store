from users.models import User

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username', 'email',
            'first_name', 'last_name',
            'user_role',
        )
