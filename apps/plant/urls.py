from django.conf.urls import url, include
from rest_framework import routers
from .viewsets import PlantViewSet, ControlViewSet, GrenhouseViewSet, CustomGet, PlantTypeList

router = routers.DefaultRouter()
router.register(r'plants', PlantViewSet, 'Plant')
router.register(r'controls', ControlViewSet, 'Control')
router.register(r'greenhouses', GrenhouseViewSet, 'Grenhouse')
router.register(r'plant-types', PlantTypeList, 'PlantType')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^custom/greenhouses/change-plant/$', CustomGet.as_view()),
]
