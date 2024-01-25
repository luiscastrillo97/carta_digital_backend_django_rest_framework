from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from users.models import User
from users.api.serializers import UserSerializer


class UserApiViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    # Override del metodo de creacion de usuario
    def create(self, request, *args, **kwargs):
        request.data["password"] = make_password(request.data["password"])
        return super().create(request, *args, **kwargs)

    # Override del metodo de actualizacion de usuario
    def partial_update(self, request, *args, **kwargs):
        password = request.data["password"]
        if password:
            request.data["password"] = make_password(password)
        else:
            request.data["password"] = request.user.password
        return super().partial_update(request, *args, **kwargs)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    # Definir el metodo para obtener la informacion del usuario logeado
    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
