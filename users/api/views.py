from users.api.serializers import UserSerializer
from users.models import User

from rest_framework import generics


__all__ = [
    'RetrieveUserView',
]


class RetrieveUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
