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
    if not layer:
        return Response(http_status.HTTP_404_NOT_FOUND)

    namespaces = {
        "wfs": "http://www.opengis.net/wfs",
        "gml": "http://www.opengis.net/gml",
        "wpGlobal": "wpGlobal" 

    }

    xml_Query = requests.get(url)
    worldpop_version = xml_Query.headers.get("QUERY_LAYERS")
    xml_text = xml_Query.text
    xml = ET.fromstring(xml_text)
    resp_body = dict()
    if "ppp_2015" in url: worldpop_version = "ppp_2015"
    elif "ppp_2016" in url: worldpop_version = "ppp_2016"
    elif "ppp_2017" in url: worldpop_version = "ppp_2017"
    elif "ppp_2018" in url: worldpop_version = "ppp_2018"
    elif "ppp_2019" in url: worldpop_version = "ppp_2019"
    elif "ppp_2020" in url: worldpop_version = "ppp_2020"

    feature_info = xml.find(f"gml:featureMember/wpGlobal:" + str(worldpop_version) + "/wpGlobal:People_Per_Pixel", namespaces=namespaces)
    resp_body['value'] = feature_info.text
    resp_body['units'] = layer.units
    return Response(resp_body, http_status.HTTP_200_OK)