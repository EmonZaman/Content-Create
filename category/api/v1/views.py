from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser

from accounts.api.v1.serializers import UserSerializer
from category.api.v1.serializers import CategorySerializer, VideoSerializer
from category.models import Category, Video


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


