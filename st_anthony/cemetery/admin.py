from django.contrib import admin

from .models import (
    ContactDetails,
    ContactMessage,
    DeceasedContactMapping,
    DeceasedDetails,
    DeceasedStatus,
    MaintenanceDetails,
    MaintenanceStatus,
    MaintenanceType,
    NewsletterSubscriber,
    Notes,
    PaymentDetails,
    PaymentStatus,
    PlotContactMapping,
    PlotDetails,
    Section,
    Users,
)


admin.site.register([
    ContactDetails,
    DeceasedContactMapping,
    DeceasedDetails,
    DeceasedStatus,
    MaintenanceDetails,
    MaintenanceStatus,
    MaintenanceType,
    Notes,
    PaymentDetails,
    PaymentStatus,
    PlotContactMapping,
    PlotDetails,
    Section,
    Users,
])


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_date')
    readonly_fields = ('created_date',)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_date')
    readonly_fields = ('created_date',)
