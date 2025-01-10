from utils.viewset import ModelViewSet, GenericViewSet
from rest_framework import serializers
from api import models


class NewsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = '__all__'


class NewsInfoView(ModelViewSet):
    queryset = models.News.objects.all()
    serializer_class = NewsInfoSerializer
