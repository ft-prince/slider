# admin.py
from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import Product, Screen ,Slider,Pdf,Videos ,Unit, DailyProductionPlan ,ProductionPlan




# Register other models
admin.site.register(Product)
admin.site.register(Screen)
admin.site.register(Slider)
admin.site.register(Pdf)
admin.site.register(Videos)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('code', 'model')

@admin.register(DailyProductionPlan)
class DailyProductionPlanAdmin(admin.ModelAdmin):
    list_display = ('date', 's_no', 'get_unit_code', 'get_unit_model', 'qty_planned', 'qty_actual')

    def get_unit_code(self, obj):
        return obj.unit.code
    get_unit_code.short_description = 'Unit Code'

    def get_unit_model(self, obj):
        return obj.unit.model
    get_unit_model.short_description = 'Unit Model'


@admin.register(ProductionPlan)
class ProductionPlanAdmin(admin.ModelAdmin):
    list_display = ('date', 's_no', 'get_unit_code', 'get_unit_model', 'qty_planned', 'qty_actual')

    def get_unit_code(self, obj):
        return obj.unit.code
    get_unit_code.short_description = 'Unit Code'

    def get_unit_model(self, obj):
        return obj.unit.model
    get_unit_model.short_description = 'Unit Model'
