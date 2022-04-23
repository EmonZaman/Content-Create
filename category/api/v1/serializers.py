from category.models import Category, Video, VideoLikes, SaveVideos, RecentShownVideos
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VideolikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLikes
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    videolikes = VideolikeSerializer(read_only=True)
    # print(likevideo)

    class Meta:
        model = Video
        fields = ['id','category', 'title','description', 'videolikes', 'video_upload_media', 'videos_thumbnail',
                  'youtube_video_link', 'video_oid']
        # fields = '__all__'
        # depth = 3


class SaveVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveVideos
        fields = '__all__'
class RecentShownSerializers(serializers.ModelSerializer):
    class Meta:
        model = RecentShownVideos
        fields = '__all__'