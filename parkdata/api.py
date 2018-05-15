from rest_framework import serializers #系列化器
from rest_framework.response import Response #构建视图，返回JSON
from rest_framework.decorators import api_view


class VideoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=1)
    class Meta:
        model = Parking #代表上面的Video模型数据
        fields = '__all__'
        depth = 3

