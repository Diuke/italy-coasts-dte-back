import datetime
import requests

import xml.etree.ElementTree as ET
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response
import simplejson
from twin_earth import models as dte_models
from twin_earth import serializers as dte_serializers
from twin_earth.copernicus_marine_services import utils as dte_utils
from rest_framework import status as http_status

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def wfs_layers(request):
    layers = dte_models.Layer.objects.filter(type=dte_models.Layer.LayerType.WFS.name, enabled=True)
    serializer = dte_serializers.LayerSerializer(layers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def wms_layers(request):
    layers = dte_models.Layer.objects.filter(type=dte_models.Layer.LayerType.WMS.name, enabled=True)
    serializer = dte_serializers.LayerSerializer(layers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def all_layers(request):
    layers = dte_models.Layer.objects.all()
    serializer = dte_serializers.LayerSerializer(layers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def categories(request):
    categories = dte_models.Category.objects.all()
    serializer = dte_serializers.BasicCategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def categories_hierarchy(request):
    start_filter_parameter = request.GET.get('start_date') #AAAA-MM-DD
    end_filter_parameter = request.GET.get('end_date') #YYYY-MM-DD
    if not start_filter_parameter and not end_filter_parameter:
        layer_group_list = dte_models.Category.objects.all()
        categories_serialized = dte_serializers.CategorySerializer(layer_group_list, many=True).data
    else:
        start_filter_date_split = start_filter_parameter.split("-")
        end_filter_date_split = end_filter_parameter.split("-")
        
        start_filter_date = datetime.date(int(start_filter_date_split[0]), int(start_filter_date_split[1]), int(start_filter_date_split[2]))
        end_filter_date = datetime.date(int(end_filter_date_split[0]), int(end_filter_date_split[1]), int(end_filter_date_split[2]))

        #initial_time_range, final_time_range
        layer_group_list = dte_models.Layer.objects.all().filter(
            (Q(initial_time_range__lte=start_filter_date) & Q(final_time_range__gte=start_filter_date)) |
            (Q(initial_time_range__lte=end_filter_date) & Q(final_time_range__gte=end_filter_date)) |
            (Q(initial_time_range__gte=start_filter_date) & Q(final_time_range__lte=end_filter_date)) |
            (Q(initial_time_range__lte=end_filter_date) & Q(final_time_range=None)) |
            (Q(initial_time_range=None) & Q(final_time_range=None))
        )
        layer_group_list = layer_group_list.filter(enabled=True)
        layer_group_list = layer_group_list.order_by("readable_name")
        layers_serialized = dte_serializers.LayerSerializer(layer_group_list, many=True).data
        categories_list = dte_models.Category.objects.all()
        categories_serialized = dte_serializers.BasicCategorySerializer(categories_list, many=True).data
        
        for category in categories_serialized:
            category["layers"] = []
            for layer in layers_serialized:
                if category is not None:
                    if layer["category"]["id"] == category["id"]:
                        category["layers"].append(layer)

    return Response(categories_serialized)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_scenario(request):
    user = request.user
    data = simplejson.loads(request.body)
    print(request.POST)
    json_string = data.get('scenario_json')
    name = data.get('name')
    scenario = dte_models.Scenario()
    scenario.name = name
    scenario.scenario_json = json_string
    scenario.owner = user
    scenario.save()
    serialized = dte_serializers.ScenarioSerializer(scenario)
    return Response(serialized.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_scenario(request):
    user = request.user
    print(request.query_params)
    scenario_id = request.query_params['id']
    scenario = dte_models.Scenario.objects.get(pk=scenario_id)
    scenario.delete()
    return Response({"message": "Deleted"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_scenarios(request):
    user = request.user
    scenarios = user.scenarios.all()
    serialized = dte_serializers.ScenarioSerializer(scenarios, many=True)
    print(scenarios)
    return Response(serialized.data)
