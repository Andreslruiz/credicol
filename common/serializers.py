from rest_framework import serializers
from . import models as m


class MunicipiosSerializer(serializers.ModelSerializer):

    text = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = m.ColombiaCities
        fields = [
            'text',
            'value',
            'name'
        ]

    def get_value(self, obj):
        return obj.name

    def get_text(self, obj):
        return obj.name
