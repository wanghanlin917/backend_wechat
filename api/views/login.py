from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.decorators import action

from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from api import models
import random
import os
from django.conf import settings
from django.core.files.storage import default_storage

from utils.filter import MineFilterBackend
from utils.viewset import GenericViewSet, ModelViewSet
from utils.ext.auth import JwtAuthentication, JwtParamAuthentication, DenyAuthentication
from utils.jwt_auth import create_token
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from utils.SendSMS import SendSMS


class SmsCodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['mobile', ]
        extra_kwargs = {
            "mobile": {
                'validators': [
                    RegexValidator(
                        regex=r'^1[3-9]\d{9}$',
                        message='请输入有效的手机号',
                        code='-1'
                    )
                ]
            }
        }


class SmsCodeView(ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = SmsCodeSerializers

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        if not serializer.is_valid():
            return Response({"code": -1, "message": serializer.errors})
        random_code = random.randint(1000, 9999)
        conn = get_redis_connection('default')
        conn.set(serializer.validated_data['mobile'], random_code, ex=60)
        return Response({'v_code': random_code})


class LoginSerializers(serializers.ModelSerializer):
    v_code = serializers.CharField(required=True, validators=[RegexValidator(r"\d{4}", message="格式错误")])

    class Meta:
        model = models.User
        fields = ['mobile', 'v_code']
        extra_kwargs = {
            "mobile": {
                'validators': [
                    RegexValidator(
                        regex=r'^1[3-9]\d{9}$',
                        message='请输入有效的手机号',
                        code='-1'
                    )
                ]
            }
        }

    def validate_v_code(self, value):
        mobile = self.initial_data.get('mobile')
        print(mobile)
        # 在redis中校验
        conn = get_redis_connection('default')
        cache_code = conn.get(mobile)
        if not cache_code:
            raise exceptions.ValidationError('手机号不存在或者验证码已失效')
        cache_code = cache_code.decode("utf-8")
        if cache_code != value:
            raise exceptions.ValidationError('验证码错误')
        conn.delete(mobile)
        return value


class LoginView(ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = LoginSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        instance = models.User.objects.filter(mobile=serializer.validated_data['mobile']).first()
        if not instance:
            serializer.validated_data.pop('v_code')
            instance = self.perform_create(serializer)
        token = create_token({"user_id": instance.id, "mobile": instance.mobile})
        # print("token", token)
        return Response({'token': token})

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance


class UserInfoSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = "__all__"
        extra_kwargs = {'id': {'read_only': True}, 'avatar_url': {'read_only': True}, 'mobile': {'read_only': True}}

    def get_avatar_url(self, obj):
        # print('ddd', self.context['request'].build_absolute_uri(obj.avatar))
        return self.context['request'].build_absolute_uri(obj.avatar)


from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin


class UserInfoView(ModelViewSet):
    authentication_classes = [JwtAuthentication, JwtParamAuthentication, DenyAuthentication]
    filter_backends = [MineFilterBackend, ]
    queryset = models.User.objects.all()
    serializer_class = UserInfoSerializer

    @action(detail=False, methods=['post'], url_path="upload")
    def upload(self, request):
<<<<<<< HEAD
        print("image", request.data.get('type'))
        type = request.data.get('type')
        upload_object = request.FILES.get('file')
=======
        # print("image", request.data.get('type'))
        # print(request.data)
        type = request.data.get('type')
        upload_object = request.FILES.get('file')
        print(type, upload_object)
>>>>>>> d24a249081f114c005a24e28749ab7f51535e7bb
        if type == "avatar":
            # print(request.FILES.get('file'))
            # print(request.FILES.get('file').name)
            # print(request.user)
            upload_url = get_upload_filename(upload_object.name)
            save_path = default_storage.save(upload_url, upload_object)
            local_url = default_storage.url(save_path)
            abs_url = request.build_absolute_uri(local_url)
            # self.lookup_field = None
            instance = models.User.objects.filter(id=request.user.get('user_id')).first()
            # print("信息", instance)
            instance.avatar = local_url
            instance.save()
            return Response({'avatar_url': abs_url})
<<<<<<< HEAD
        else:
            print("正面", request.data)
=======
        elif type == "repairImg":
            upload_url = get_upload_filename(upload_object.name, "repairImg")
            save_path = default_storage.save(upload_url, upload_object)
            local_url = default_storage.url(save_path)
            abs_url = request.build_absolute_uri(local_url)
            # instance = models.RepairImg.objects.create(url=local_url)
            return Response({"url": abs_url, "localUrl": local_url})
        else:
            # print(type(request.data))
            # print("data",upload_object)
>>>>>>> d24a249081f114c005a24e28749ab7f51535e7bb
            upload_url = get_upload_filename(upload_object.name, 'identify')
            save_path = default_storage.save(upload_url, upload_object)
            local_url = default_storage.url(save_path)
            abs_url = request.build_absolute_uri(local_url)
            return Response({"url": abs_url, "localUrl": local_url})


def get_upload_filename(filename, folder="avatar"):
    upload_path = os.path.join(settings.UPLOAD_PATH, folder)
    file_path = os.path.join(upload_path, filename)
    return default_storage.get_available_name(file_path)
