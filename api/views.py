from rest_framework import generics
from api.models import Video
from api.serializers import VideoSerializer

# Create your views here.
class VideoList(generics.ListAPIView):
    queryset = Video.objects.all().order_by('-publish_datetime')
    serializer_class = VideoSerializer