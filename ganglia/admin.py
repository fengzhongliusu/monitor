from django.contrib import admin
from ganglia.models import Resource,Metric

# Register your models here.

class MetricInline(admin.TabularInline):
	model = Metric

class ResAdmin(admin.ModelAdmin):
	fieldsets = [
	   ('name',	{'fields':['res_name']}),
	   ('type',	{'fields':['res_type'],'classes':['collapse']}),
	   ('hostname',	{'fields':['res_hostname'],'classes':['collapse']}),
	]
	inlines = [MetricInline]
	list_display = ('res_name','res_type','res_hostname')


admin.site.register(Resource,ResAdmin)
