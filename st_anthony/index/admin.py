from django.contrib import admin
from .models import Notes, DeceasedStatus, Section, ContactDetails, MaintenanceStatus, MaintenanceType, PlotDetails, DeceasedDetails, DeceasedContactMapping,PlotContactMapping, MaintenanceDetails, PaymentStatus, PaymentDetails

admin.site.register(Notes)
admin.site.register(DeceasedStatus)
admin.site.register(Section)
admin.site.register(ContactDetails)
admin.site.register(MaintenanceStatus)
admin.site.register(MaintenanceType)
admin.site.register(PlotDetails)
admin.site.register(DeceasedDetails)
admin.site.register(DeceasedContactMapping)
admin.site.register(PlotContactMapping)
admin.site.register(MaintenanceDetails)
admin.site.register(PaymentStatus)
admin.site.register(PaymentDetails)