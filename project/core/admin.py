from django.contrib import admin

from project.core import models

admin.site.register(models.Plugin)
admin.site.register(models.Category)

# TODO: REGISTER ALL DJANGO MODELS FOR THE CORE APP
# Register your models here.
