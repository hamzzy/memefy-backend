# from rest_framework import parsers, viewsets, generics
# from rest_framework import status
#
# from rest_framework.response import Response
# from rest_framework_simplejwt.views import TokenObtainPairView
#
# from .Serializer import RegisterSerializer, LoginSerializer
# from .models import CustomUser
#
#
# class RegisterView(generics.GenericAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = RegisterSerializer
#
#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(serializer.data)
#         return Response({
#             'msg': 'CustomUser Registered',
#             'status': status.HTTP_200_OK
#         }
#         )
#
#
#
# class LoginView(generics.GenericAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )
