from django.db.models import fields
from rest_framework import serializers
from twin_earth import models as dte_models

class BasicCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = dte_models.Category
        fields = "__all__"

class LayerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    layer_name = serializers.CharField()
    readable_name = serializers.CharField()
    description = serializers.CharField()
    keywords = serializers.CharField()
    type = serializers.CharField()
    category = BasicCategorySerializer()
    frequency = serializers.CharField()
    initial_time_range = serializers.DateField()
    final_time_range = serializers.DateField()
    parameters = serializers.CharField()
    source = serializers.CharField()
    service_url = serializers.CharField()
    metadata_url = serializers.CharField()
    legend_url = serializers.CharField()
    more_data_url = serializers.CharField()
    copyright = serializers.CharField()

    class Meta:
        model = dte_models.Layer
        fields = "__all__"

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    layers = serializers.SerializerMethodField()

    def get_layers(self, obj):
        children_list = obj.layers.all()
        return LayerSerializer(children_list, many=True).data

    class Meta:
        model = dte_models.Category
        fields = "__all__"