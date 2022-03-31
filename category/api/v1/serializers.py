from category.models import Category, Video, VideoLikes, SaveVideos
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        # depth = 1


class VideolikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLikes
        fields = '__all__'
class SaveVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveVideos
        fields = '__all__'