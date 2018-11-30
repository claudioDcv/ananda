\
from django.contrib import admin
from .models import Plant, Control, Greenhouse, PlantType


@admin.register(PlantType)
class PlantTypeAdmin(admin.ModelAdmin):
	pass


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):

	list_display = ('id', 'name', 'code', 'user', 'rating', 'greenhouse')
	def save_model(self, request, obj, form, change):
		if not obj.user_id:
			obj.user = request.user
		obj.save()

	def get_queryset(self, request):
                qs = super(PlantAdmin, self).get_queryset(request)
                if request.user.is_superuser:
                        return qs
                return qs.filter(user=request.user)


	def formfield_for_foreignkey(self, db_field, request, **kwargs):
        	if db_field.name == "greenhouse":
            		kwargs["queryset"] = Greenhouse.objects.filter(user=request.user)
       		return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):

	def get_queryset(self, request):
                qs = super(ControlAdmin, self).get_queryset(request)
                if request.user.is_superuser:
                        return qs
                return qs.filter(plant__user=request.user)


	def formfield_for_foreignkey(self, db_field, request, **kwargs):
                if db_field.name == "plant":
                        kwargs["queryset"] = Plant.objects.filter(user=request.user)
                return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Greenhouse)
class GreenhouseAdmin(admin.ModelAdmin):

	list_display = ('id', 'name', 'code', 'user', 'x', 'y')
	def save_model(self, request, obj, form, change):

		# import ipdb; ipdb.set_trace()
		if not obj.user_id:
			obj.user = request.user
		obj.save()

	def get_queryset(self, request):
        	qs = super(GreenhouseAdmin, self).get_queryset(request)
        	if request.user.is_superuser:
            		return qs
        	return qs.filter(user=request.user)
