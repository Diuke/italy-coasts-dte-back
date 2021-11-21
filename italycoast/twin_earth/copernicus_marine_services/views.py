import datetime
from os import name
from django import utils
import requests
import xml.etree.ElementTree as ET

from twin_earth.copernicus_marine_services import utils as copernicus_utils
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status as http_status
from django.db.models import Q
from rest_framework.response import Response
from django.shortcuts import render
from twin_earth import models as dte_models
from twin_earth import serializers as dte_serializers

@api_view(['GET'])
@permission_classes([AllowAny])
def update_layers(request):
    wms_list = [
        #MEDSEA_ANALYSISFORECAST_PHY_006_013
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-cur-an-fc-d",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-cur-an-fc-h",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-cur-an-fc-hts",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-cur-an-fc-m",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-cur-an-fc-qm",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-mld-an-fc-d",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-mld-an-fc-d",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-mld-an-fc-m",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-sal-an-fc-d",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-sal-an-fc-h",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-sal-an-fc-hts",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-sal-an-fc-m",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-ssh-an-fc-d",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-ssh-an-fc-hts",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-ssh-an-fc-m",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-ssh-an-fc-qm",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-tem-an-fc-d",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-tem-an-fc-h",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-tem-an-fc-hts",
        "https://nrt.cmems-du.eu/thredds/wms/med-cmcc-tem-an-fc-m",
        #MEDSEA_MULTIYEAR_PHY_006_004
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-cur-int-m",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-cur-rean-d",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-cur-rean-h",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-cur-rean-m",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-mld-int-m",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-mld-rean-d",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-mld-rean-m",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-sal-int-m",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-sal-rean-d",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-sal-rean-m",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-ssh-int-m",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-ssh-rean-d",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-ssh-rean-h",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-ssh-rean-m",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-tem-int-m",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-tem-rean-d",
        "https://my.cmems-du.eu/thredds/wms/med-cmcc-tem-rean-m",
        #MEDSEA_ANALYSISFORECAST_WAV_006_017
        "https://nrt.cmems-du.eu/thredds/wms/med-hcmr-wav-an-fc-h",
        #MEDSEA_MULTIYEAR_WAV_006_012
        "https://my.cmems-du.eu/thredds/wms/med-hcmr-wav-rean-h",
        #MEDSEA_ANALYSISFORECAST_BGC_006_014
        "https://nrt.cmems-du.eu/thredds/wms/med-ogs-bio-an-fc-d",
        "https://nrt.cmems-du.eu/thredds/wms/med-ogs-bio-an-fc-m",
        "https://nrt.cmems-du.eu/thredds/wms/med-ogs-car-an-fc-d",
        "https://nrt.cmems-du.eu/thredds/wms/med-ogs-car-an-fc-m",
        "https://nrt.cmems-du.eu/thredds/wms/med-ogs-co2-an-fc-d",
        "https://nrt.cmems-du.eu/thredds/wms/med-ogs-co2-an-fc-m",
        "https://nrt.cmems-du.eu/thredds/wms/med-ogs-nut-an-fc-d",
        "https://nrt.cmems-du.eu/thredds/wms/med-ogs-nut-an-fc-m",
        "https://nrt.cmems-du.eu/thredds/wms/med-ogs-pft-an-fc-d",
        "https://nrt.cmems-du.eu/thredds/wms/med-ogs-pft-an-fc-m",
        #MEDSEA_MULTIYEAR_BGC_006_008
        "https://my.cmems-du.eu/thredds/wms/med-ogs-bio-rean-fc-d",
        "https://my.cmems-du.eu/thredds/wms/med-ogs-bio-rean-fc-m",
        "https://my.cmems-du.eu/thredds/wms/med-ogs-car-rean-fc-d",
        "https://my.cmems-du.eu/thredds/wms/med-ogs-car-rean-fc-m",
        "https://my.cmems-du.eu/thredds/wms/med-ogs-co2-rean-fc-d",
        "https://my.cmems-du.eu/thredds/wms/med-ogs-co2-rean-fc-m",
        "https://my.cmems-du.eu/thredds/wms/med-ogs-nut-rean-fc-d",
        "https://my.cmems-du.eu/thredds/wms/med-ogs-nut-rean-fc-m",
        "https://my.cmems-du.eu/thredds/wms/med-ogs-pft-rean-fc-d",
        "https://my.cmems-du.eu/thredds/wms/med-ogs-pft-rean-fc-m",
        #SEALEVEL_MED_PHY_MDT_L4_STATIC_008_066
        "https://my.cmems-du.eu/thredds/wms/cmems_obs-sl_med_phy-mdt_my_l4-0.0417deg_P20Y",
        #SEALEVEL_MED_PHY_L4_NRT_OBSERVATIONS_008_050
        "https://nrt.cmems-du.eu/thredds/wms/dataset-duacs-nrt-medsea-merged-allsat-phy-l4",
        #SEALEVEL_MED_PHY_L4_REP_OBSERVATIONS_008_051
        "https://my.cmems-du.eu/thredds/wms/dataset-duacs-rep-medsea-merged-allsat-phy-l4",
        #OCEANCOLOUR_MED_CHL_L4_NRT_OBSERVATIONS_009_041
        "https://nrt.cmems-du.eu/thredds/wms/dataset-oc-med-chl-multi-l4-chl_1km_monthly-rt-v02",
        "https://nrt.cmems-du.eu/thredds/wms/dataset-oc-med-chl-multi-l4-interp_1km_daily-rt-v02",
        "https://nrt.cmems-du.eu/thredds/wms/dataset-oc-med-chl-olci_a-l4-chl_1km_monthly-rt-v02",
        "https://nrt.cmems-du.eu/thredds/wms/dataset-oc-med-chl-olci-l4-chl_300m_monthly-rt",
        #OCEANCOLOUR_MED_BGC_HR_L4_NRT_009_211
        "https://nrt.cmems-du.eu/thredds/wms/cmems_obs_oc_med_bgc_tur-spm-chl_nrt_l4-hr-mosaic_P1D-m",
        #SST_EUR_PHY_L4_NRT_010_031
        "https://nrt.cmems-du.eu/thredds/wms/METEOFRANCE-EUR-SST-L4-NRT-OBS_FULL_TIME_SERIE",
        #
        "https://nrt.cmems-du.eu/thredds/wms/SST_MED_SST_L4_NRT_OBSERVATIONS_010_004_a_V2",
        "https://nrt.cmems-du.eu/thredds/wms/SST_MED_SST_L4_NRT_OBSERVATIONS_010_004_c_V2",
        "https://nrt.cmems-du.eu/thredds/wms/SST_MED_SSTA_L4_NRT_OBSERVATIONS_010_004_b",
        "https://nrt.cmems-du.eu/thredds/wms/SST_MED_SSTA_L4_NRT_OBSERVATIONS_010_004_d"
        
    ]
    copernicus_utils.update_layers(wms_list)
    return Response(200)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_list_of_parameter_values(request, layer_id, parameter):
    try:
        layer = dte_models.Layer.objects.get(id=int(layer_id))
    except Exception as ex:
        return Response(http_status.HTTP_404_NOT_FOUND)

    start_time = None
    end_time = None
    if request.GET.get("start_time") and request.GET.get("end_time"):
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")

    urlSuffix = "?request=GetCapabilities&service=WMS&VERSION=1.3.0&layer=" + layer.layer_name
    url = layer.service_url + urlSuffix
    namespaces = {
        "opengis": "http://www.opengis.net/wms" 
    }

    xml_GetCapabilities = requests.get(url)
    xml_text = xml_GetCapabilities.text
    xml = ET.fromstring(xml_text)

    #["WMS_Capabilities"]["Capability"][0]["Layer"][0]["Layer"][0]["Layer"][0]["Dimension"]
    parameter_values = xml.findall(f"opengis:Capability/opengis:Layer/opengis:Layer/opengis:Layer/opengis:Dimension[@name='{parameter}']", namespaces=namespaces)
    
    params = dict()
    for p in parameter_values:
        param_object = {
            "default": p.get("default"),
            "units": p.get("units"),
            "name": p.get("name"),
            "values": p.text.strip().split(",")
        }
        if param_object["name"] == "time":
            complete_time_list = copernicus_utils.format_time_intervals(param_object["values"])
            param_object["values"] = complete_time_list
            param_object["values"].reverse()
        
        params[param_object["name"]] = param_object

    return Response(param_object, http_status.HTTP_200_OK)