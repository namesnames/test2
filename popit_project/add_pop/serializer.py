from rest_framework import serializers
from .models import ChemiPop,PythonPop,DjangoPop,EnginMathPop,TOEICPop


class ChemiPopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemiPop
        fields = "__all__"
        read_only_fields = ('id',)
class ChemiPoplikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemiPop
        fields = ['likes']

class PythonPopSerializer(serializers.ModelSerializer):
    class Meta:
        model = PythonPop
        fields = "__all__"
        read_only_fields = ('id',)

class DjangoPopSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoPop
        fields = "__all__"
        read_only_fields = ('id',)
        
class EnginMathPopSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnginMathPop
        fields = "__all__"
        read_only_fields = ('id',)
        
class TOEICPopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TOEICPop
        fields = "__all__"
        read_only_fields = ('id',)