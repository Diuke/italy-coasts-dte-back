import datetime
from os import name
from django import utils
import requests
import xml.etree.ElementTree as ET

from twin_earth.copernicus_marine_services import utils as copernicus_utils
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status as http_status
from rest_framework.response import Response
from twin_earth import models as dte_models
from twin_earth import serializers as dte_serializers

@api_view(['POST'])
@permission_classes([AllowAny])
def get_data(request):
    
    data = request.data
    layer_id = data.get('layer_id')
    url = data.get('request_url')   

    layer = dte_models.Layer.objects.all().get(pk=layer_id)
    print(url)
    if not layer:
        return Response(http_status.HTTP_404_NOT_FOUND)

    namespaces = {
        "wfs": "http://www.opengis.net/wfs",
        "gml": "http://www.opengis.net/gml",
        "wpGlobal": "wpGlobal" 

    }

    xml_Query = requests.get(url)
    xml_text = xml_Query.text
    xml = ET.fromstring(xml_text)
    print(xml)
    resp_body = dict()

    feature_info = xml.find(f"gml:featureMember/wpGlobal:ppp_2020/wpGlobal:People_Per_Pixel", namespaces=namespaces)
    print(feature_info)
    print(feature_info.text)
    resp_body['value'] = feature_info.text
    resp_body['units'] = layer.units
    return Response(resp_body, http_status.HTTP_200_OK)