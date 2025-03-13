from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
admin.site.register(Worker)
admin.site.register(Company)
admin.site.register(Work)
admin.site.register(Progress)
admin.site.register(ProgressItem)

admin.site.register(DateforProgress)
admin.site.register(Progresstype)
admin.site.register(User)
admin.site.register(Attendence_date)
admin.site.register(WorkerExpanses)
admin.site.register(WorkerExpansesDetail)
admin.site.register(Avans)
admin.site.register(Jarima)
admin.site.register(Premya)
admin.site.register(DateforExpanse)
admin.site.register(Expanse)
admin.site.register(ExpanseName)