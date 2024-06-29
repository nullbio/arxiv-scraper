from django.contrib import admin

from project.plugins.arxiv import models

admin.site.register(models.Archive)
admin.site.register(models.MonthlyArchive)
admin.site.register(models.TotalEntriesMismatch)
admin.site.register(models.Paper)
