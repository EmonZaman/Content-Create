from contextvars import Token

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib.auth import get_user_model
from rest_framework import request, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext as _
from accounts.api.v1 import serializers
from accounts.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, GenericAPIView
from accounts.api.v1.serializers import AccountsSerializer, RegisterSerializer, UserSerializer, GoogleLoginSerializer


class UserListApiView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountsSerializer


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer


class LoginAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = self.authenticate(email=email, password=password)
        except Exception as e:
            user = None
            print("auth error", e)
        if user:
            response = self.get_serializer(instance=user)
            return Response(response.data, status=200)
        else:
            return Response({"Could not authenticate user"}, status=404)

    def authenticate(self, email=None, password=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
            if user.check_password(password):  # check valid password
                return user  # return user to be authenticated
        except user_model.DoesNotExist:  # no matching user exists
            return None


class CurrentUser(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        current_user = request.user
        data = UserSerializer(current_user).data
        return Response(data, status=200)


class AbstractBaseLoginView(GenericAPIView):
    authentication_classes = []

    class Meta:
        abstract = True

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # logger.error(get_debug_str(request, request.user, serializer.errors))
            raise ValidationError(serializer.errors)

        user = serializer.validated_data.get('user')
        created = serializer.validated_data.get('created')

        user_serializer = UserSerializer(instance=user, context={'request': request})
        token, _ = Token.objects.get_or_create(user=user)

        resp = {
            'token': token.key,
            'created': created,
            'user_info': user_serializer.data
        }
        return Response(resp, status=status.HTTP_200_OK)


class GoogleLoginView(AbstractBaseLoginView):
    serializer_class = GoogleLoginSerializer
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
