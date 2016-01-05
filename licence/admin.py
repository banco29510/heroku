from django.contrib import admin

from licence.models import Licence

class LicenceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Licence, LicenceAdmin)

