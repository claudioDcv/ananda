from django.core.serializers import serialize
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Plant, Control, Greenhouse, PlantType, PlantType
from .errors import OwnerError, ConstrainError, GreenhouseSpaceNotExistError


class PlantTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = PlantType
		fields = ('id', 'name', 'code')


class GreenhouseSerializer(serializers.ModelSerializer):

    plant_count = serializers.SerializerMethodField()

    class Meta:
        model = Greenhouse
        fields = ('id', 'name', 'code', 'modified_date', 'created_date', 'x', 'y', 'user', 'plant_count')

    def get_plant_count(self, obj):
        return obj.plant_set.count()

    def create(self, validated_data):

        req = self.context.get('request')
        validated_data['user'] = req.user
        instance = Greenhouse.objects.create(**validated_data)
        return instance

class PlantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plant
        fields = ('id', 'name', 'code', 'modified_date', 'created_date', 'rating', 'user', 'x', 'y', 'greenhouse')

    # def update(self, instance, validated_data):
    #     import ipdb; ipdb.set_trace()
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.created = validated_data.get('created', instance.created)
    #     return instance

    def create(self, validated_data):

        req = self.context.get('request')
        validated_data['user'] = req.user

        try:
            instance = Plant.objects.create(**validated_data)
            return instance
        except ConstrainError as identifier:
            raise identifier
        except GreenhouseSpaceNotExistError as identifier:
            raise identifier



class ControlSerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(read_only=True, source="plant.name")
    # user = serializers.CharField(read_only=True, source="plant.user.pk")
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Control
        fields = ('id', 'name', 'captured_date', 'humidity', 'pH', 'description', 'plant', 'plant_name', 'created_date', 'modified_date', 'temperature', 'user_id')

    def get_user_id(self, obj):
        return obj.plant.user_id

    def create(self, validated_data):

        req = self.context.get('request')
        user_id = req.user.pk

        plant = validated_data.pop('plant')

        # Si el usuario no es dueño de la planta se retorna un error no_owner
        if plant.user_id == user_id:
            validated_data['plant'] = plant
            instance = Control.objects.create(**validated_data)
            return instance
        else:
            raise OwnerError('plant_no_owner')
