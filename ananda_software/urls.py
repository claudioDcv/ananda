from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from apps.plant.urls import urlpatterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


urlpatterns = [
    path('api/admin/', admin.site.urls),
    url(r'^api/api-auth/', include('rest_framework.urls')),
    url(r'^api/api-token-auth/', obtain_jwt_token),
    url(r'^api/api-token-refresh/', refresh_jwt_token),
     url(r'^api/api-token-verify/', verify_jwt_token),
    url('api/', include(urlpatterns)),
]

