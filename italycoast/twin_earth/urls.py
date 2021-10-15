from django.urls import path
from twin_earth import views

urlpatterns = [
    path('layers/wms', views.wms_layers, name='layers_wms'),
    path('layers/wfs/', views.wfs_layers, name='layers_wfs'),    
    path('layers/all/', views.all_layers, name='layers_all'),    

    path('categories/', views.categories, name='categories'),    
    path('categories_hierarchy/', views.categories_hierarchy, name='categories_hierarchy'),    
]