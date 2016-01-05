##
# \file admin.py
# \brief Liste des actions de base pour le panel admin
# \date 02/05/15
#
from django.contrib import admin


from software.models import Software

class SoftwareAdmin(admin.ModelAdmin):
    pass


admin.site.register(Software, SoftwareAdmin)


