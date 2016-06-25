from django.contrib import admin
from gensite.gendbs import models

class TypeAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'desc')
	
class ALLAdmin(admin.ModelAdmin):
	list_display = ('id', 'typedb', 'name', 'desc')

class ExpAdmin(admin.ModelAdmin):
	list_display = ('id', 'typedb','name', 'users', 'refdb', 'extraction', 'specific', 'start', 'end','is_execute', 'desc')
class XXAdmin(admin.ModelAdmin):
	list_display = ('name', 'typedb', 'position_start', 'position_end', 'position_top', 'desc')

class ResultAdmin(admin.ModelAdmin):
	list_display = ('id','exp_id', 'tax_id', 'accuracy', 'bootstrap', 'remain')

admin.site.register(models.TypeDB, TypeAdmin)
admin.site.register(models.Classifier, TypeAdmin)
admin.site.register(models.Extraction, TypeAdmin)
admin.site.register(models.Tax, TypeAdmin)

admin.site.register(models.RefDB, ALLAdmin)
admin.site.register(models.Vregion, XXAdmin)
admin.site.register(models.Primer, XXAdmin)
admin.site.register(models.HyperVariable)
admin.site.register(models.Result, ResultAdmin)
admin.site.register(models.Experiment, ExpAdmin)

