import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response
from django.shortcuts import render
from twin_earth import models as dte_models
from twin_earth import serializers as dte_serializers

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def wfs_layers(request):
    layers = dte_models.Layer.objects.filter(type=dte_models.Layer.LayerType.WFS.name)
    serializer = dte_serializers.LayerSerializer(layers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def wms_layers(request):
    layers = dte_models.Layer.objects.filter(type=dte_models.Layer.LayerType.WMS.name)
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
    start_filter_parameter = request.GET.get('start_date') #DD-MM-AAAA
    end_filter_parameter = request.GET.get('end_date') #DD-MM-AAAA
    if not start_filter_parameter and not end_filter_parameter:
        layer_group_list = dte_models.Category.objects.all()
        serialized = dte_serializers.CategorySerializer(layer_group_list, many=True).data
    else:
        start_filter_date_split = start_filter_parameter[0].split("-")
        end_filter_date_split = end_filter_parameter[0].split("-")
        
        start_filter_datetime = datetime.date(start_filter_date_split[2], start_filter_date_split[1], start_filter_date_split[0])
        end_filter_date = datetime.datetime(end_filter_date_split[2], end_filter_date_split[1], end_filter_date_split[0])

        #initial_time_range, final_time_range
        layer_group_list = dte_models.Category.objects.all().filter(
            (Q(initial_time_range__gte=start_filter_datetime) & Q(initial_time_range__lte=end_filter_date)) | 
            (Q(final_time_range__gte=start_filter_datetime) & Q(final_time_range__lte=end_filter_date))
        )
        serialized = dte_serializers.CategorySerializer(layer_group_list, many=True).data

    return Response(serialized)