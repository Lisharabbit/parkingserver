from rest_framework import serializers
from .models import Finetreepredict,Blockquery
class PredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finetreepredict
        fields = ('blcokid', 'period_h', 'period_m', 'predicted')

class BlockquerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Blockquery
        fields = ('streemarker','blcokid')