from rest_framework import serializers

from api import models
from utils.viewset import ModelViewSet, GenericViewSet


class NewsInfoSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    class Meta:
        model = models.News
        fields = '__all__'

class NewsInfoView(ModelViewSet):
    queryset = models.News.objects.all()
    serializer_class = NewsInfoSerializer
