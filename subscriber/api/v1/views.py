from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from subscriber.api.v1.serializers import SubscriberSerializer
from subscriber.models import Subscriber


class SubscriberListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

class SubscriberDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
