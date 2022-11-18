from twin_earth.models import Layer
from twin_earth.copernicus_marine_services import utils as cmems_utils
from twin_earth.copernicus_land_service import utils as clms_utils

def build_wms_get_feature_info_url(service_url, params):
    url = service_url + "?"
    url += "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&"
    for param in params:
        url += param["key"] + "=" + param["value"] + "&"

#params -> {bbox: [min_lat, min_lng, max_lat, max_lng], dimensions: {dim1: value, dim2: value}}
def build_layer_feature_info_url(layer, params):
    try:
        url = ""

        if layer.source == "Copernicus Marine Services":
            url = cmems_utils.build_copernicus_marine_service_url(layer, params)

        elif layer.source == "Copernicus Land Service":
            url = clms_utils.build_copernicus_land_service_url(layer, params)
        else:
            return None

        #&QUERY_LAYERS=chl&LAYERS=chl&BBOX=1252344.271424327%2C5205055.8781073615%2C1291480.0299063374%2C5244191.636589372&CRS=EPSG%3A3857&time=2020-04-01T12%3A00%3A00.000Z&elevation=-3625.703857421875&INFO_FORMAT=text%2Fxml&I=39&J=154&WIDTH=256&HEIGHT=256&STYLES=
        return url
    except Exception as ex:
        return None