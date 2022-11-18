import simplejson

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from twin_earth.models import Layer
from rest_framework.response import Response
from rest_framework import status as http_status
from twin_earth.copernicus_marine_services import wrapper as cmems_wrapper
from twin_earth.copernicus_land_service import wrapper as clms_wrapper

POINT_REQUEST_TYPE = "point"
DEPTH_REQUEST_TYPE = "depth_profile"
AREA_REQUEST_TYPE = "area"
TIME_SERIES_REQUEST_TYPE = "time_series"

@api_view(['GET'])
@permission_classes([AllowAny])
def get_list_of_parameter_values(request, layer_id, parameter):
    try:
        layer = Layer.objects.get(id=int(layer_id))
    except Exception as ex:
        return Response(http_status.HTTP_404_NOT_FOUND)

    params = {}
    #route the request to the specific wrapper
    if layer.source == "Copernicus Marine Services":
        params = cmems_wrapper.get_parameters(layer, parameter)
    elif layer.source == "Copernicus Land Monitoring Service":
        return Response("Incorrect Source", http_status.HTTP_400_BAD_REQUEST)
    elif layer.source == "WorldPop":
        return Response("Incorrect Source", http_status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Incorrect Layer", http_status.HTTP_400_BAD_REQUEST)

    return Response(params, http_status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_data(request):
    try:
        data = simplejson.loads(request.body)
        params = data["params"]
        #params example
        # "params": {
        #     "bbox": [978393.9620502554,5518141.945963444,988177.9016707579,5527925.8855839465],
        #     "elevation": -1.0182366371154785,
        #     "time": "2022-10-01T00:00:00.000Z"
        # }
        data_request_type = data["type"] # point, area, time_series, depth_profile
        layer_id = int(data["layer_id"])
        layer = Layer.objects.get(id=layer_id)

        #route the request to the specific wrapper
        if layer.source == "Copernicus Marine Services":
            if data_request_type == POINT_REQUEST_TYPE:
                response_data = cmems_wrapper.get_data(layer, params)

            elif data_request_type == AREA_REQUEST_TYPE:
                response_data = cmems_wrapper.get_area_statistics(layer, params)
                
            elif data_request_type == DEPTH_REQUEST_TYPE:
                response_data = cmems_wrapper.get_depth_profile(layer, params)

            elif data_request_type == TIME_SERIES_REQUEST_TYPE:
                response_data = cmems_wrapper.get_time_series(layer, params)
                
            else:
                return Response("Incorrect Request Type", http_status.HTTP_400_BAD_REQUEST)

        elif layer.source == "Copernicus Land Monitoring Service":
            if data_request_type == POINT_REQUEST_TYPE:
                response_data = clms_wrapper.get_data(layer, params)
                
            else:
                return Response("Incorrect Request Type", http_status.HTTP_400_BAD_REQUEST)

        elif layer.source == "WorldPop":
            return Response("Not supported", http_status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Incorrect Layer", http_status.HTTP_400_BAD_REQUEST)

        return Response(response_data, http_status.HTTP_200_OK)
    except Exception as ex:
        print(ex.with_traceback())
        return Response("error", http_status.HTTP_400_BAD_REQUEST)