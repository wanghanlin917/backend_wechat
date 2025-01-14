from api.models import User
from utils.viewset import GenericViewSet, ModelViewSet
from rest_framework import serializers
from rest_framework.response import Response
from django.core.validators import RegexValidator
import re
from utils.SendSMS import SendSMS


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile']
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


class LoginView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializers

    def list(self, request, *args, **kwargs):
        print(request.query_params.get('mobile'))

        queryset = self.filter_queryset(self.get_queryset())
        print(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
