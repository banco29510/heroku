from django.contrib import admin

from instrument.models import Instrument

class InstrumentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Instrument, InstrumentAdmin)
