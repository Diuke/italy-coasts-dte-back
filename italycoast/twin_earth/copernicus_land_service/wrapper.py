import requests
import xml.etree.ElementTree as ET

from twin_earth.copernicus_land_service import utils as clms_utils
from twin_earth import models as dte_models

def get_data(layer, params):
    url = clms_utils.build_copernicus_land_service_url(layer, params)
    print(url)
    
    resp_body = {}
    if layer.type == dte_models.Layer.LayerType.ARCGIS_ImageServer:
        json_response = requests.get(url).json()
        if layer.layer_name == "HRL_BuiltUp_2018:IBU_MosaicSymbology":
            resp_body = {
                "value": json_response["value"],
                "units": clms_utils.built_up_categories()[int(json_response["value"])]
            }
        elif layer.layer_name == "HRL_ForestType_2018:FTY_MosaicSymbology":
            resp_body = {
                "value": json_response["value"],
                "units": clms_utils.forest_type_codes()[int(json_response["value"])]
            }

        elif layer.layer_name == "HRL_WaterWetness_2018:WAW_MosaicSymbology":
            resp_body = {
                "value": json_response["value"],
                "units": clms_utils.waw_codes()[int(json_response["value"])]
            }

        else: 
            resp_body = {
                "value": json_response["value"],
                "units": layer.units
            }
        

    elif layer.type == dte_models.Layer.LayerType.ARCGIS_MapServer:
        json_response = requests.get(url).json()
        if layer.readable_name == "Imperviousness Density (IMD) 2015" or layer.readable_name == "Imperviousness Density (IMD) 2012" or layer.readable_name == "Imperviousness Density (IMD) 2009":
            resp_body = {
                "value": json_response["results"][0]["attributes"]["Pixel Value"],
                "units": json_response["results"][0]["attributes"]["Classnames"]
            }

        elif layer.readable_name == "Imperviousness Density (IMD) 2006":
            resp_body = {
                "value": json_response["results"][0]["attributes"]["Pixel Value"],
                "units": "% Imperviousness Value"
            }

        elif layer.readable_name == "Water & Wetness (WAW) 2015":
            resp_body = {
                "value": json_response["results"][0]["attributes"]["Pixel Value"],
                "units": json_response["results"][0]["attributes"]["class_name"]
            }

        else:
            resp_body = {
                "value": json_response["results"][0]["attributes"]["Pixel Value"],
                "units": json_response["results"][0]["attributes"]["Class_Name"]
            }

    else:
        xml_Query = requests.get(url)
        xml_text = xml_Query.text
        xml = ET.fromstring(xml_text)
        resp_body = dict()
        namespaces = {
            "esri_wms": "http://www.esri.com/wms" 
        }

        if layer.layer_name == "Coastal_Zones_2018_vector57533":
            feature_info = xml.find(f"esri_wms:FIELDS", namespaces=namespaces)
            code = feature_info.get("CODE_5_18")
            resp_body['value'] = code
            resp_body['units'] = clms_utils.coastal_zones_codes()[int(code)]

        elif layer.layer_name == "Coastal_Zones_2018_raster65095":
            feature_info = xml.find(f"esri_wms:FIELDS", namespaces=namespaces)
            code = feature_info.get("PixelValue")
            resp_body['value'] = code
            resp_body['units'] = clms_utils.coastal_zones_codes()[int(code)]
            
        elif layer.layer_name == "Coastal_Zones_2012_raster55645":
            feature_info = xml.find(f"esri_wms:FIELDS", namespaces=namespaces)
            code = feature_info.get("PixelValue")
            resp_body['value'] = code
            resp_body['units'] = clms_utils.coastal_zones_codes()[int(code)]

        elif layer.layer_name == "Coastal_Zones_2012_vector53031":
            feature_info = xml.find(f"esri_wms:FIELDS", namespaces=namespaces)
            code = feature_info.get("CODE_5_12")
            resp_body['value'] = code
            resp_body['units'] = clms_utils.coastal_zones_codes()[int(code)]

        elif layer.layer_name == "13": #CLC 2018 vector
            feature_info = xml.find(f"esri_wms:FIELDS", namespaces=namespaces)
            code = feature_info.get("Code_18")
            resp_body['value'] = code
            resp_body['units'] = clms_utils.corine_land_cover_codes()[int(code)]

        elif layer.layer_name == "12": #CLC 2018 raster
            feature_info = xml.find(f"esri_wms:FIELDS", namespaces=namespaces)
            print(feature_info)
            code = feature_info.get("Raster.CODE_18")
            label = feature_info.get("Raster.LABEL3")
            resp_body['value'] = code
            resp_body['units'] = label

        else:
            resp_body = xml_Query

    return resp_body
