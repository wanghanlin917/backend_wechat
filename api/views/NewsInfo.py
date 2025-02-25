from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend

from api import models
from utils.viewset import ModelViewSet, GenericViewSet
from utils.ext.auth import JwtAuthentication, JwtParamAuthentication, DenyAuthentication
from rest_framework.response import Response


class NewsInfoSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = models.News
        fields = '__all__'


class NewsInfoView(ModelViewSet):
    queryset = models.News.objects.all()
    serializer_class = NewsInfoSerializer


class AddHouseInfoSerializer(serializers.ModelSerializer):
    idcardFrontUrl = serializers.SerializerMethodField()
    idcardBackUrl = serializers.SerializerMethodField()

    class Meta:
        model = models.HouseInformation
        fields = ['id', 'name', 'point', 'building', 'room', 'mobile', 'gender', 'idcardFront', 'idcardBack', 'user',
                  'status', 'idcardFrontUrl', 'idcardBackUrl']
        # fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'status': {'read_only': True},
            'id': {'read_only': True},
            'idcardFrontUrl': {'read_only': True},
            'idcardBackUrl': {'read_only': True}
        }

    def get_idcardFrontUrl(self, obj):
        return self.context['request'].build_absolute_uri(obj.idcardFront)

    def get_idcardBackUrl(self, obj):
        return self.context['request'].build_absolute_uri(obj.idcardBack)


from rest_framework.mixins import CreateModelMixin, UpdateModelMixin


class AddHouseInfoView(ModelViewSet):
    authentication_classes = [JwtAuthentication, JwtParamAuthentication, DenyAuthentication]
    queryset = models.HouseInformation.objects.all()
    serializer_class = AddHouseInfoSerializer

    def create(self, request, *args, **kwargs):
        # print("数据", request.data)
        id = request.data.get("id")
        if id:
            instance = models.HouseInformation.objects.filter(id=id).first()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data)

    def perform_create(self, serializer):
        # print("添加。。。。。", self.request.user)
        serializer.save(user_id=self.request.user['user_id'])

    def perform_update(self, serializer):
        serializer.save()


class WarrantSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = models.HouseInformation
        fields = ['id', 'name']

    def get_name(self, obj):
        return obj.point + obj.building + obj.room


class WarrantFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # print(request.user)
        # print(queryset.filter(**{'user_id': request.user.get('user_id'),'status': 2}))
        return queryset.filter(**{'user_id': request.user.get('user_id'), 'status': 2})


class WarrantyView(ModelViewSet):
    authentication_classes = [JwtAuthentication, JwtParamAuthentication, DenyAuthentication]
    queryset = models.HouseInformation.objects.all()
    serializer_class = WarrantSerializer
    filter_backends = [WarrantFilter, ]


class RepairProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RepairProject
        fields = "__all__"


class RepairProjectView(ModelViewSet):
    authentication_classes = [JwtAuthentication, JwtParamAuthentication, DenyAuthentication]
    queryset = models.RepairProject.objects.all()
    serializer_class = RepairProjectSerializer
