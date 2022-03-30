from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from subscriber.api.v1.serializers import SubscriberSerializer
from subscriber.models import Subscriber


class SubscriberListAPIView(ListCreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

class SubscriberDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
