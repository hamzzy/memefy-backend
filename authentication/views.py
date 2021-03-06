import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import parsers, viewsets, generics, permissions
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
# from templated_email import InlineImage
# from templated_email import get_templated_mail

from rest_framework.response import Response

from memeapp import settings
from permission import IsOwnerOrReadOnly
from .Serializer import CustomUserSerializer, LoginSerializer, ResetPasswordEmailRequestSerializer, \
    EmailVerificationSerializer, SetNewPasswordSerializer, UserAccountChangePasswordSerializer, UserAccountUpdateSerializer
from .Utils import activation_email, password_reset_email
from .models import CustomUser


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    parser_classes = (JSONParser,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # get_verified = CustomUser.objects.get(email=request.data['email'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class RegisterView(generics.GenericAPIView):
    parser_classes = (JSONParser,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        if request.is_secure():
            protocol = 'https://'
        else:
            protocol = 'http://'
        absurl = protocol + "localhost:3000/activate-email/"+str(token)
        context = {
            'url': absurl,
            'user': user,
        }
        activation_email(to=user, context=context)

        return Response({
            'msg': 'CustomUser Registered',
        }, status=status.HTTP_200_OK)


class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def post(self, request):
        token = request.data['token']
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:

            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


# class ResendEmailVerification(generics.GenericAPIView):
#     serializer_class = CustomUserSerializer
#
#     # permission_classes = ()
#
#     def get(self, request):
#         user = CustomUser.objects.get(email=request.user.email)
#         token = RefreshToken.for_user(user).access_token
#         current_site = get_current_site(request).domain
#         relativeLink = reverse('email-verify')
#         absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
#         email_body = 'Hi ' + user.name + \
#                      ' Use the link below to verify your email \n' + absurl
#         data = {'email_body': email_body, 'to_email': user.email,
#                 'email_subject': 'Verify your email'}
#
#         Util.send_email(data)
#         return Response({'msg': 'Successfully resend verification'}, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = "/password-reset-confirm/" +uidb64+"/"+token
            if request.is_secure():
                protocol = 'https://'
            else:
                protocol = 'http://'
            absurl = protocol + 'localhost:3000' + relativeLink

            context = {
                'url': absurl,
                'user': user
            }

            password_reset_email(to=user, context=context)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'email cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class UserAccountChangePasswordView(generics.CreateAPIView):
    """"Change the password of logged in user.
    post:
    Request to change the password of the user, it requires to provide *old_password* and *new_password*
    parameters.
    """

    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    serializer_class = UserAccountChangePasswordSerializer


class UserAccountUpdateView(generics.UpdateAPIView):
    """"Change the password of logged in user.
    post:
    Request to change the password of the user, it requires to provide *old_password* and *new_password*
    parameters.
    """

    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserAccountUpdateSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': "data updated"}, status=status.HTTP_200_OK)
