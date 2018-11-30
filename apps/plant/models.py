from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .errors import ConstrainError, GreenhouseSpaceNotExistError


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}) {1}'.format(self.code, self.name)

    class Meta:
        abstract = True


class Greenhouse(BaseModel):
    user = models.ForeignKey(User, editable = False, on_delete = False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    x = models.IntegerField(blank=True, null=True, default=0)
    y = models.IntegerField(blank=True, null=True, default=0)



class PlantType(BaseModel):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=100)

class Plant(BaseModel):
    type = models.ForeignKey(PlantType, on_delete=models.CASCADE)
    greenhouse = models.ForeignKey(Greenhouse, on_delete=models.CASCADE)
    user = models.ForeignKey(User, editable = False, on_delete = False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    # category = models.CharField(max_length=10, choices=CATEGORIES_CHOICES)

    def __str__(self):
        return self.name

    # def validate_unique(self, exclude=None):
    #     qs = Room.objects.filter(name=self.name)
    #     if qs.filter(zone__site=self.zone__site).exists():
    #         raise ValidationError('Name must be unique per site')

    def clean(self, *args, **kwargs):
        # Validacion de estapacion al guardar una planta

        x = self.x
        y = self.y
        greenhouse = self.greenhouse

        # se valida que es espacio en el invernadero exista
        # solo el espacio 0 - 0 se puede utilizar pues es una planta
        # asignada a invernadero sin espacio fijo
        if (
                greenhouse.x < x or greenhouse.y < y or x < 0 or y < 0
            ) or (
                y > 0 and x == 0 # no se permite y valido con x 0
            ) or (
                x > 0 and y == 0 # no se permite y 0 e y valido
            ):
            raise GreenhouseSpaceNotExistError('greenhouse_space_not_exist')

        # si x = 0, y = 0 entonces se guarda en invernadero
        # pero sin espacio asignado
        if x == 0 and y == 0:
            super(BaseModel, self).clean(*args, **kwargs)
        else:
            # si ya existe una planta en el lugar no se permite el guardado
            older_plant = Plant.objects.filter(
                x=x,
                y=y,
                greenhouse=greenhouse,
            ).first()

            # solo arroja error si los ids son distinstos
            # si los ids son iguales es posible cambiar el espacio ya que es un update
            if older_plant:
                if older_plant.pk is not self.pk:
                    raise ConstrainError('there_is_already_a_plant')

        # guardado normal
        super(BaseModel, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super(BaseModel, self).save(*args, **kwargs)
        except ConstrainError as identifier:
            raise identifier
        except GreenhouseSpaceNotExistError as identifier:
            raise identifier

    # class Meta:
    #     unique_together = (('x', 'y', 'greenhouse'),)


class Control(BaseModel):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    humidity = models.FloatField()
    pH = models.FloatField()
    temperature = models.FloatField()
    captured_date = models.DateTimeField()

    def __str__(self):
        return '{0} | {1} {2}'.format(self.name, self.plant, self.plant_id)
