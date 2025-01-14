from api.models import User
from utils.viewset import GenericViewSet, ModelViewSet
from rest_framework import serializers
from rest_framework.response import Response
from django.core.validators import RegexValidator
from utils.SendSMS import SendSMS


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['mobile']
        extra_kwargs = {
            "mobile": [RegexValidator(r"\d{11}", message="格式错误")]
        }
    def validate_mobile(self, value):
        print("dddd",value)
        # queryset = User.objects.filter(mobile=value)
        # if not queryset.exists():
        #     pass



class LoginView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializers

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
