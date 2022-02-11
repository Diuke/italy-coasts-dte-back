from django.urls import path
from twin_earth import views as twin_earth_views
from twin_earth.copernicus_marine_services import views as copernicus_marine_services_views
from twin_earth.copernicus_land_service import views as copernicus_land_services_views
from twin_earth.worldpop import views as worldpop_views

urlpatterns = [
    path('layers/wms', twin_earth_views.wms_layers, name='layers_wms'),
    path('layers/wfs/', twin_earth_views.wfs_layers, name='layers_wfs'),    
    path('layers/all/', twin_earth_views.all_layers, name='layers_all'),    

    path('categories/', twin_earth_views.categories, name='categories'),    
    path('categories_hierarchy/', twin_earth_views.categories_hierarchy, name='categories_hierarchy'),    

    # Copernicus marine services
    path('copernicus_marine_services/list_parameter_values/<str:layer_id>/<str:parameter>', copernicus_marine_services_views.get_list_of_parameter_values, name='categories_hierarchy'),    
    #path('copernicus_marine_services/update_layers', copernicus_marine_services_views.update_layers, name='copernicus_marine_services_update_layers'),

    #Get data
    path('copernicus_marine_services/getData', copernicus_marine_services_views.get_data, name='copernicus_marine_services_get_data'),

    # Copernicus Land Monitoring Service
    path('copernicus_land_services/getData', copernicus_land_services_views.get_data, name='copernicus_land_services_views_get_data'),

    # Worldpop
    path('worldpop/getData', worldpop_views.get_data, name='worldpop_views_get_data'),

]