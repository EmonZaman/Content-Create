from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from accounts.api.v1.serializers import UserSerializer
from accounts.models import User
from category.api.v1.serializers import CategorySerializer, VideoSerializer
from category.models import Category, Video

from datetime import datetime, timedelta


class CategoryListApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class VideoListApiView(ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    # parser_classes = (FormParser, MultiPartParser)


class VideoDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class category_content(ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category', None)

        return Video.objects.filter(category__name=category)


class LastSevenDaysUserListAPIView(ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=7))
        return queryset
class LastSevenDaySubscriberListAPIView(ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=7), is_pro=True)
        return queryset
class UserAndSubscriberCountAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        response = {}
        # total_user= self.request.query_params.get('User', None)
        total_pro_user = self.request.query_params.get('total_pro_user', None)
        pro_user_seven = self.request.query_params.get('pro_user_seven', None)
        pro_user_today = self.request.query_params.get('pro_user_today', None)
        users_last_seven_days= self.request.query_params.get('users_last_seven_days', None)
        total_users = self.request.query_params.get('total_users', None)
        users_today = self.request.query_params.get('users_today', None)

        if total_pro_user=="true":
            pro_user_count = User.objects.filter(is_pro=True).count()
            response['Total_pro_users']= pro_user_count
        if pro_user_seven=="true":
            pro_user_count = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=7), is_pro=True).count()
            response['pro_users_last_seven_days']= pro_user_count
        if pro_user_today=="true":
            pro_user_count = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=1), is_pro=True).count()
            response['pro_users_today']= pro_user_count
        if users_last_seven_days == "true":
            pro_user_count = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=7)).count()
            response['users_last_seven_days'] = pro_user_count
        if total_users == "true":
            pro_user_count = User.objects.count()
            response['total_users'] = pro_user_count

        if users_today == "true":
            pro_user_count = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=1)).count()
            response['users_today'] = pro_user_count



        return Response(response)



