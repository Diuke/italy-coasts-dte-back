import datetime
from os import name
from urllib import response
from django import utils
import requests
import xml.etree.ElementTree as ET
import numpy as np
import simplejson

from twin_earth.copernicus_marine_services import utils as copernicus_utils
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status as http_status
from rest_framework.response import Response
from twin_earth import models as dte_models
from twin_earth import serializers as dte_serializers
from django.contrib.gis.geos import GEOSGeometry, Polygon

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
    params = get_parameters(layer, parameter)
    return Response(params, http_status.HTTP_200_OK)

def get_parameters(layer, parameter):
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
    
    param_object = {
        "default": parameter_values[0].get("default"),
        "units": parameter_values[0].get("units"),
        "name": parameter_values[0].get("name"),
        "values": parameter_values[0].text.strip().split(",")
    }
    if param_object["name"] == "time":
        complete_time_list = copernicus_utils.format_time_intervals(param_object["values"])
        param_object["values"] = complete_time_list
        param_object["values"].reverse()
    
    return param_object


@api_view(['POST'])
@permission_classes([AllowAny])
def get_data(request):
    
    data = request.data
    layer_id = data.get('layer_id')
    url = data.get('request_url')   

    layer = dte_models.Layer.objects.all().get(pk=layer_id)
    if not layer:
        return Response(http_status.HTTP_404_NOT_FOUND)

    if layer.source == 'Copernicus Marine Services':
        xml_Query = requests.get(url)
        xml_text = xml_Query.text
        xml = ET.fromstring(xml_text)
        resp_body = dict()
        feature_info = xml.find(f"FeatureInfo/value")
        resp_body['value'] = feature_info.text
        resp_body['units'] = layer.units
        return Response(resp_body, http_status.HTTP_200_OK)
        
    else:
        return Response(http_status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_time_series(request):
    data = request.data
    #start time - end time - elevation?
    layer_id = data.get('layer_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    elevation = data.get('elevation')
    base_url = data.get('base_url')

    layer = dte_models.Layer.objects.all().get(pk=layer_id)
    times = get_parameters(layer, "time")

    times_counter = 0
    resp_body = {
        "x": [],
        "y": [],
        "units": layer.units 
    }

    url = base_url + '&time=' + str(start_date) + "/" + str(end_date)
    if elevation:
        url += '&elevation=' + str(elevation)
    xml_Query = requests.get(url)
    xml_text = xml_Query.text
    xml = ET.fromstring(xml_text)
    
    feature_infos = xml.findall("FeatureInfo")

    for feature in feature_infos:
        feature_info_time = feature.find("time").text
        feature_info_value = feature.find("value").text
        resp_body['x'].append(feature_info_time)
        resp_body['y'].append(feature_info_value)

    return Response(resp_body, http_status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_depth_profile(request):
    data = request.data
    #start time - end time - elevation?
    layer_id = data.get('layer_id')
    time = data.get('time')
    base_url = data.get('base_url')

    layer = dte_models.Layer.objects.all().get(pk=layer_id)
    elevations = get_parameters(layer, "elevation")

    resp_body = {
        "x": [],
        "y": [],
        "units": layer.units 
    }
    for elevation in elevations['values']:

            url = base_url + '&'
            url += 'time=' + str(time)
            url += '&elevation=' + str(elevation)
            xml_Query = requests.get(url)
            xml_text = xml_Query.text
            xml = ET.fromstring(xml_text)
            
            feature_info = xml.find(f"FeatureInfo/value")
            feature_info_value = feature_info.text
            if feature_info_value == "none": #break if the request produce no values
                break

            resp_body['y'].append(elevation)
            resp_body['x'].append(feature_info_value)            

    return Response(resp_body, http_status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_area_statistics(request):
    data = request.data
    #default resolution
    x_resolution = 20
    y_resolution = 20
    bbox_string = data.get("bbox")
    bbox = bbox_string.split(",") # [min_x, min_y, max_x, max_y]
    time = data.get("time")
    histogram_classes = data.get("classes")
    elevation = data.get("elevation")
    polygon_geojson = simplejson.loads(data.get("polygon"))
    polygon_geometry = polygon_geojson["features"][0]["geometry"]
    polygon_geometry["crs"] = {
        "type": "name",
        "properties": {
            "name": "EPSG:3857"
        }
    }
    geojson = simplejson.dumps(polygon_geometry)
    polygon_feature = GEOSGeometry(geojson)
    
    bbox_feature = Polygon.from_bbox(bbox)

    layer_id = data.get('layer_id')
    layer = dte_models.Layer.objects.all().get(pk=layer_id)

    resolution = data.get("resolution")
    if resolution == "high":
        x_resolution = 20
        y_resolution = 20
    elif resolution == "low":
        x_resolution = 10
        y_resolution = 10
    else:
        x_resolution = 10
        y_resolution = 10

    start_x = float(bbox[0])
    end_x = float(bbox[2])
    start_y = float(bbox[1])
    end_y = float(bbox[3])

    x_len = abs(end_x - start_x)
    y_len = abs(end_y - start_y)
    x_step = x_len / x_resolution
    y_step = y_len / y_resolution

    #Build base url
    base_url = layer.service_url + "?" + "SERVICE=WMS&VERSION=1.1.1&REQUEST=GetFeatureInfo&INFO_FORMAT=text/xml&SRS=EPSG:3857"
    base_url += "&HEIGHT=" + str(y_resolution) + "&WIDTH=" + str(x_resolution)
    base_url += "&BBOX=" + bbox_string
    base_url += "&QUERY_LAYERS=" + layer.layer_name
    base_url += "&time=" + time
    if elevation:
        base_url += "&elevation=" + elevation
    
    response_matrix = np.zeros((x_resolution, y_resolution))
    list_data = []
    cells_with_values = 0
    
    for x in range(x_resolution):
        for y in range(y_resolution):
            x_min = start_x + (x * x_step)
            x_max = x_min + x_step
            y_min = start_y + (y * y_step)
            y_max = y_min + y_step
            cell_geometry = f"SRID=3857;POLYGON (({x_min} {y_min}, {x_min} {y_max}, {x_max} {y_max}, {x_max} {y_min}, {x_min} {y_min}))"
            cell_polygon = GEOSGeometry(cell_geometry)
            
            if cell_polygon.intersects(polygon_feature):
                request_url = base_url + "&X=" + str(x) + "&Y=" + str(y)

                xml_Query = requests.get(request_url)
                xml_text = xml_Query.text
                xml = ET.fromstring(xml_text)
                
                feature_info = xml.find(f"FeatureInfo/value")
                feature_info_value = feature_info.text
                try:
                    numerical_value = float(feature_info_value)
                    cells_with_values += 1
                    list_data.append(numerical_value)

                except Exception as ex:
                    numerical_value = np.NaN

                response_matrix[x, y] = numerical_value
            else:
                response_matrix[x, y] = np.NaN

    median = np.nanmedian(response_matrix)
    stdev = np.nanstd(response_matrix)
    min_value = np.nanmin(response_matrix)
    max_value = np.nanmax(response_matrix)
    avg_value = np.nanmean(response_matrix)

    
    resp = {
        "sampling": simplejson.dumps(response_matrix.tolist(), ignore_nan=True),
        "histogram": np.histogram(list_data, histogram_classes),
        "min": min_value,
        "max": max_value,
        "median": median,
        "standard_deviation": stdev,
        "average": avg_value,
        "total_samples_with_value": cells_with_values
    }
    
    return Response(resp, http_status.HTTP_200_OK)
            