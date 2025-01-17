from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import exceptions

from django.core.validators import RegexValidator
from django_redis import get_redis_connection
from api import models
import random

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
    class Meta:
        model = models.User
        fields = "__all__"


class UserInfoView(ModelViewSet):
    authentication_classes = [JwtAuthentication, JwtParamAuthentication, DenyAuthentication]
    queryset = models.User.objects.all()
    serializer_class = UserInfoSerializer
