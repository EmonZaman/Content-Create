# from contextvars import Token
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib.auth import get_user_model
from rest_framework import request, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext as _
from accounts.api.v1 import serializers
from accounts.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, GenericAPIView
from accounts.api.v1.serializers import AccountsSerializer, RegisterSerializer, UserSerializer, GoogleLoginSerializer
import stripe
from datetime import timedelta
import datetime
import pytz

stripe.api_key = 'sk_test_51KeXrmExsbXRovz76iC19UwNt6uq4XfEjMZIIwfHoz8JW6Sq9UFLk8PfmpqHtE49a27bWjXgeLgRViJC4LpBoSUM001fgxvoRx'

utc = pytz.UTC


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
    permission_classes = [IsAuthenticated, ]

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


class CheckPro(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = self.request.user
        print(user.free_expiry_date)
        user.free_expiry_date = user.date_joined + timedelta(15)
        user.save()
        print(user.free_expiry_date)
        # user.pro_expiry_date = utc.localize(user.pro_expiry_date)
        # user.free_expiry_date = utc.localize(user.free_expiry_date)
        free_expairy = user.free_expiry_date.replace(tzinfo=None)

        print("pro expiry date")
        # print(pro_expiry)
        if free_expairy >= datetime.datetime.now():
            return Response(True)
        elif user.pro_expiry_date is not None:
            pro_expiry = user.pro_expiry_date.replace(tzinfo=None)
            if pro_expiry >= datetime.datetime.now():
                return Response(True)
            else:
                user.is_pro = False
                user.save()
                return Response(False)

        else:
            user.is_pro = False
            user.save()
            return Response(False)

        # try:
        #     user = User.objects.get(username=username) # retrieve the user using username
        # except User.DoesNotExist:
        #     return Response(data={'message':False}) # return false as user does not exist
        # else:
        #     return Response(data={'message':True}) # Otherwise, return True
