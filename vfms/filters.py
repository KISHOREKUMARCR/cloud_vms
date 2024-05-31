import django_filters
from .models import *
class VideoFileFilter(django_filters.FilterSet):
    class Meta:
        model=VideoFiles
        fields=['ProjectName','StationName','LICate','videostatus']

class VideoDetectFilter(django_filters.FilterSet):
    class Meta:
        model=VideoFiles
        fields=['ProjectName','StationName',]        