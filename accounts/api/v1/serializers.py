from urllib.error import HTTPError
from allauth.account import app_settings as allauth_settings
from allauth.account.signals import user_logged_in
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils import timezone
from rest_framework import serializers
from accounts.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _



class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1

# class UserProfileDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         exclude = ['user']
#         # depth = 1


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'password dont match'})

        user.set_password(password)
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    # userprofile= UserProfileDetailSerializer()


    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"read_only": True}
        }
        depth = 1

    def get_name(self, obj: User):
        google_profile = obj.get_google_profile_data()
        return google_profile.get('name')

    def get_picture(self, obj: User):
        google_profile = obj.get_google_profile_data()
        return google_profile.get('picture')

    def update(self, instance, validated_data):
        return validated_data

    def get_token(self, obj):
        token = Token.objects.get_or_create(user=obj)
        return token[0].key

class GoogleLoginSerializer(serializers.Serializer):
    auth_code = serializers.CharField(label=_('Authorization code'), required=False)
    access_token = serializers.CharField(label=_('Access Token'), required=False)
    referer = serializers.EmailField(label=_('Referer'), required=False)

    def _get_request(self):
        request = self.context.get('request')
        if not isinstance(request, HttpRequest):
            request = request._request
        return request

    def get_social_login(self, adapter, app, token, response):
        request = self._get_request()
        social_login = adapter.complete_login(request, app, token, response=response)
        social_login.token = token
        return social_login

    def validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()

        if not view:
            raise serializers.ValidationError(
                _("View is not defined, pass it as a context variable")
            )

        adapter_class = getattr(view, 'adapter_class', None)
        client_class = getattr(view, 'client_class', None)

        if not adapter_class:
            raise serializers.ValidationError(_("Define adapter_class in view"))

        if not client_class:
            raise serializers.ValidationError(_("Define client_class in view"))

        adapter = adapter_class(request)
        app = adapter.get_provider().get_app(request)
        callback_url = adapter.get_callback_url(request, app)
        provider = adapter.get_provider()
        scope = provider.get_scope(request)

        auth_code = attrs.get('auth_code')
        access_token = attrs.get('access_token')

        if auth_code:
            client = client_class(
                request,
                app.client_id, app.secret,
                adapter.access_token_method,
                adapter.access_token_url,
                callback_url,
                scope,
                scope_delimiter=adapter.scope_delimiter,
                headers=adapter.headers,
                basic_auth=adapter.basic_auth
            )

            try:
                token = client.get_access_token(auth_code)
            except OAuth2Error as e:
                raise serializers.ValidationError({'auth_code': e})

            access_token = token['access_token']

        elif access_token:
            token = {'access_token': access_token}

        else:
            raise serializers.ValidationError({'auth_code': 'Auth Code or Access Token is required'})

        social_token = adapter.parse_token(token)
        social_token.app = app

        current_dt = timezone.now()

        try:
            login = self.get_social_login(adapter, app, social_token, access_token)
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_("Incorrect value"))

        if not login.is_existing:
            if getattr(allauth_settings, 'UNIQUE_EMAIL', False):
                account_exists = get_user_model().objects.filter(
                    email=login.user.email,
                ).exists()
                if account_exists:
                    raise serializers.ValidationError(
                        _("User is already registered with this e-mail address.")
                    )

            login.lookup()
            login.save(request, connect=True)

        user = login.account.user
        created = user.date_joined >= current_dt
        attrs['user'], attrs['created'] = user, created
        user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


# noinspection PyMethodMayBeStatic
# class UserSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField(label=_('Name'))
#     picture = serializers.SerializerMethodField(label=_('Photo URL'))
#
#     class Meta:
#         model = User
#         fields = [
#             'id', 'username', 'name', 'first_name', 'last_name', 'email', 'picture'
#         ]
#
#     def get_name(self, obj: User):
#         google_profile = obj.get_google_profile_data()
#         return google_profile.get('name')
#
#     def get_picture(self, obj: User):
#         google_profile = obj.get_google_profile_data()
#         return google_profile.get('picture')
#
#     def update(self, instance, validated_data):
#         return validated_data
