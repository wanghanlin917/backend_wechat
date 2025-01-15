from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import exceptions

from django.core.validators import RegexValidator
from django_redis import get_redis_connection
from api.models import User
import random

from utils.viewset import GenericViewSet, ModelViewSet

from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from utils.SendSMS import SendSMS


class SmsCodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile',]
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
    queryset = User.objects.all()
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
        model = User
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
            },
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
    queryset = User.objects.all()
    serializer_class = LoginSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
