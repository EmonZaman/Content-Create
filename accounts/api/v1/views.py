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

stripe.api_key = 'sk_test_51KeXrmExsbXRovz76iC19UwNt6uq4XfEjMZIIwfHoz8JW6Sq9UFLk8PfmpqHtE49a27bWjXgeLgRViJC4LpBoSUM001fgxvoRx'


class UserListApiView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountsSerializer


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # def put(self, request, *args, **kwargs):
    #     item= self.request.query_params.get('item', None)
    #     price = self.request.query_params.get('price', None)
    #
    #     if item == 'true':
    #         if price is not None:
    #             YOUR_DOMAIN = "http://127.0.0.1:8000"
    #             checkout_session = stripe.checkout.Session.create(
    #                 # payment_method_type=['card'],
    #                 line_items=[
    #                     {
    #                         'price_data': {
    #                             'currency': 'usd',
    #                             'unit_amount': 30000,
    #                             'product_data': {
    #                                 'name': 'checkout',
    #
    #                             },
    #                         },
    #                         # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
    #                         # 'price': '{{PRICE_ID}}',
    #                         'quantity': 1,
    #                     },
    #                 ],
    #                 mode='payment',
    #                 # success_url=YOUR_DOMAIN + '/success/',
    #                 # cancel_url=YOUR_DOMAIN + '/cancel/',
    #             )
    #             # return JsonResponse({
    #             #     'id': checkout_session.id
    #             #
    #             # })
    #             return redirect(checkout_session.url, code=303)


# class UserProfileDetailApiView(ListCreateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileDetailSerializer

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
    permission_classes = [IsAuthenticated,]

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
