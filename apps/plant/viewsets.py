from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import PlantSerializer, ControlSerializer, GreenhouseSerializer, PlantTypeSerializer
from .models import Plant, Control, Greenhouse, PlantType
from .errors import OwnerError, ConstrainError, GreenhouseSpaceNotExistError


class PlantTypeList(viewsets.ViewSet):
	permission_classes = (IsAuthenticated,)

	def list(self, request):
        	queryset = PlantType.objects.all()
        	serializer = PlantTypeSerializer(queryset, many=True)
        	return Response(serializer.data)


class GrenhouseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    model = Greenhouse
    serializer_class = GreenhouseSerializer

    def get_queryset(self):
        queryset = Greenhouse.objects.all().filter(user=self.request.user)
        return queryset


class PlantViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    model = Plant
    serializer_class = PlantSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('greenhouse',)

    def get_queryset(self):
        queryset = Plant.objects.all().filter(user=self.request.user)
        return queryset
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ConstrainError as identifier:
            return Response({'error': str(identifier)}, status=status.HTTP_401_UNAUTHORIZED)
        except GreenhouseSpaceNotExistError as identifier:
            return Response({'error': str(identifier)}, status=status.HTTP_401_UNAUTHORIZED)


class ControlViewSet(viewsets.ModelViewSet):
    """
    ### Query String
    - plant = int
    - captured_date_from = date(yyyy-mm-dd)
    - captured_date_to = date(yyyy-mm-dd)

    ```
    ?plant=1&captured_date_from=2018-12-21&captured_date_to=2018-12-22
    ```
    """
    permission_classes = (IsAuthenticated,)
    model = Control
    serializer_class = ControlSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('plant',)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except OwnerError as identifier:
            return Response({'error': str(identifier)}, status=status.HTTP_401_UNAUTHORIZED)


    def get_queryset(self):
        
        qs = self.request.query_params

        queryset = Control.objects.all().filter(plant__user=self.request.user)

        # gt - lt filters
        captured_date_from = qs.get('captured_date_from', False)
        captured_date_to = qs.get('captured_date_to', False)
        if captured_date_from and captured_date_to:
            queryset = queryset.filter(captured_date__range=[captured_date_from, captured_date_to])


        plant_id = qs.get('plant', False)
        if plant_id:
            queryset = queryset.filter(plant=plant_id)
        return queryset.order_by('captured_date')

## CUSTOMERS APIS ###

 
class CustomGet(APIView):
    """
    - PUT cambiar 2 plantas de posicion dentro de un mismo invernadero
    ```json
    {
        "from":  1,
        "to": { "x": 2, "y": 1, "greenhouse": 1 }
    }
    ```
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        return Response({"success": True, "content": "Hello World!"})

    def post(self, request, format=None):

        return Response({"success": True, "content": "Hello World!"})
    
    def put(self, request, format=None):
        """
            - cambiar 2 plantas de posicion dentro de un mismo invernadero
        """
        plant_from = Plant.objects.filter(pk=request.data.get('from')).first()
        plant_to = Plant.objects.filter(**request.data.get('to')).first()

        plant_to_x = request.data.get('to').get('x')
        plant_to_y = request.data.get('to').get('y')
        plant_to_greenhouse = request.data.get('to').get('greenhouse')

        plant_from_x = plant_from.x
        plant_from_y = plant_from.y
        plant_from_greenhouse = plant_from.greenhouse
        # si existe planta en el lugar se deja nulo su lugar pero
        # se mantiene en el invernadero
        if plant_to:
            plant_to.x = 0
            plant_to.y = 0
            plant_to.save()

        plant_from.x = plant_to_x
        plant_from.y = plant_to_y
        plant_from.save()

        if plant_to:
            plant_to.x = plant_from_x
            plant_to.y = plant_from_y
            plant_to.save()

        return Response({"success": True, "content": "Hello World!"})
