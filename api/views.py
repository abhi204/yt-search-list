from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from api.models import Video
from api.serializers import VideoSerializer


# Create your views here.
class VideoList(generics.ListAPIView):
    queryset = Video.objects.all().order_by('-publish_datetime') # get queryset ordered by publish date
    serializer_class = VideoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description'] # fields to apply search filter for
    ordering_fields = '__all__' # all fields can be used for ordering
    ordering = ['-publish_datetime'] # default ordering
