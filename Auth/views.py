from rest_framework import parsers, viewsets
from rest_framework import response
from rest_framework import status
from rest_framework.response import Response

from .Serializer import RegisterSerializer
from .models import User


class RegisterView(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(
            user_data,
            status=status.HTTP_200_OK
        )





class LoginView(viewsets.ModelViewSet):
    def post(self,request):
        pass