from django.contrib import admin
from rbac import models

admin.site.register(models.User)
admin.site.register(models.Menu)
admin.site.register(models.Action)
admin.site.register(models.Permission)
admin.site.register(models.Permission2Action2Group)
admin.site.register(models.Group)
admin.site.register(models.User2Group)
