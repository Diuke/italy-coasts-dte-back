
def build_wms_get_feature_info_url(service_url, params):
    url = service_url + "?"
    url += "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&"
    for param in params:
        url += param["key"] + "=" + param["value"] + "&"

    #&QUERY_LAYERS=chl&LAYERS=chl&BBOX=1252344.271424327%2C5205055.8781073615%2C1291480.0299063374%2C5244191.636589372&CRS=EPSG%3A3857&time=2020-04-01T12%3A00%3A00.000Z&elevation=-3625.703857421875&INFO_FORMAT=text%2Fxml&I=39&J=154&WIDTH=256&HEIGHT=256&STYLES=
    return url