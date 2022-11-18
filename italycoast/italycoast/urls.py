from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from auth_app import urls as auth_urls
from twin_earth import urls as dte_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include(auth_urls.urlpatterns)),
    path('api/dte/', include(dte_urls.urlpatterns))
]
