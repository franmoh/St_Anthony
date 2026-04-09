from django.db import models
from django.contrib.auth.models import User


class Notes(models.Model):
    """Base model - no dependencies"""
    note_id = models.AutoField(primary_key=True)
    note = models.CharField(max_length=4000)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='notes_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='notes_modified', null=True, blank=True)

    class Meta:
        db_table = 'Notes'

    def __str__(self):
        return self.note[:50]


class DeceasedStatus(models.Model):
    """Base model - no dependencies"""
    deceased_status_id = models.AutoField(primary_key=True)
    deceased_status_constant = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='deceased_status_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='deceased_status_modified', null=True, blank=True)

    class Meta:
        db_table = 'DeceasedStatus'

    def __str__(self):
        return self.deceased_status_constant


class Section(models.Model):
    """Base model - no dependencies"""
    section_id = models.AutoField(primary_key=True)
    section_constant = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sections_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sections_modified', null=True, blank=True)

    class Meta:
        db_table = 'Section'
        indexes = [
            models.Index(fields=['section_constant', 'section_id'], name='ixSectionConstant'),
        ]

    def __str__(self):
        return self.section_constant


class ContactDetails(models.Model):
    """Depends on Notes and User"""
    contact_details_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    note = models.ForeignKey(Notes, on_delete=models.PROTECT, null=True, blank=True, db_column='NoteID')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contact_details_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contact_details_modified', null=True, blank=True)

    class Meta:
        db_table = 'ContactDetails'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MaintenanceStatus(models.Model):
    """Base model - no dependencies"""
    maintenance_status_id = models.AutoField(primary_key=True)
    maintenance_status_constant = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='maintenance_status_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='maintenance_status_modified', null=True, blank=True)

    class Meta:
        db_table = 'MaintenanceStatus'

    def __str__(self):
        return self.maintenance_status_constant


class MaintenanceType(models.Model):
    """Base model - no dependencies"""
    maintenance_type_id = models.AutoField(primary_key=True)
    maintenance_type_constant = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='maintenance_type_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='maintenance_type_modified', null=True, blank=True)

    class Meta:
        db_table = 'MaintenanceType'

    def __str__(self):
        return self.maintenance_type_constant


class PlotDetails(models.Model):
    """Depends on Section, MaintenanceStatus, Notes, User"""
    PLOT_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Sold', 'Sold'),
        ('Unknown', 'Unknown'),
    ]
    
    plot_details_id = models.AutoField(primary_key=True)
    plot_id = models.IntegerField()
    section = models.ForeignKey(Section, on_delete=models.PROTECT, db_column='SectionID')
    row = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)
    side = models.CharField(max_length=100, null=True, blank=True)
    niche = models.CharField(max_length=100, null=True, blank=True)
    maintenance_status = models.ForeignKey(MaintenanceStatus, on_delete=models.PROTECT, db_column='MaintenanceStatusID')
    plot_status = models.CharField(max_length=20, choices=PLOT_STATUS_CHOICES, default='Available')
    is_available = models.BooleanField(default=True)
    note = models.ForeignKey(Notes, on_delete=models.PROTECT, null=True, blank=True, db_column='NoteID')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='plots_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='plots_modified', null=True, blank=True)

    class Meta:
        db_table = 'PlotDetails'
        indexes = [
            models.Index(fields=['maintenance_status'], name='ix_MaintenanceStatus'),
            models.Index(fields=['note'], name='ix_Notes'),
            models.Index(fields=['section'], name='idx_plotdetails_section'),
            models.Index(fields=['plot_id'], name='idx_plotdetails_plot'),
        ]

    def __str__(self):
        return f"Plot {self.plot_id} - Section {self.section.section_constant}"


class DeceasedDetails(models.Model):
    """Depends on PlotDetails, DeceasedStatus, Notes, User"""
    deceased_details_id = models.AutoField(primary_key=True)
    plot = models.ForeignKey(PlotDetails, on_delete=models.PROTECT, db_column='PlotID')
    zone_id = models.IntegerField(default=0)
    deceased_status = models.ForeignKey(DeceasedStatus, on_delete=models.PROTECT, db_column='DeceasedStatusID')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    date_buried = models.DateField(null=True, blank=True)
    dob_year = models.PositiveSmallIntegerField(null=True, blank=True)
    dob_month = models.PositiveSmallIntegerField(null=True, blank=True)
    dob_day = models.PositiveSmallIntegerField(null=True, blank=True)
    dod_year = models.PositiveSmallIntegerField(null=True, blank=True)
    dod_month = models.PositiveSmallIntegerField(null=True, blank=True)
    dod_day = models.PositiveSmallIntegerField(null=True, blank=True)
    note = models.ForeignKey(Notes, on_delete=models.PROTECT, null=True, blank=True, db_column='NoteID')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='deceased_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='deceased_modified', null=True, blank=True)

    class Meta:
        db_table = 'DeceasedDetails'
        unique_together = ['plot', 'zone_id']
        indexes = [
            models.Index(fields=['plot', 'deceased_status'], name='ix_DeceasedPlotStatus'),
            models.Index(fields=['date_buried'], name='ix_DateBuried'),
            models.Index(fields=['dob_year'], name='idx_dobyear'),
            models.Index(fields=['dod_year'], name='idx_dodyear'),
            models.Index(fields=['plot'], name='idx_deceased_plot'),
            models.Index(fields=['zone_id'], name='idx_deceased_zone'),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.plot}"


class DeceasedContactMapping(models.Model):
    """Depends on DeceasedDetails, ContactDetails, User"""
    deceased_contact_mapping_id = models.AutoField(primary_key=True)
    deceased_details = models.ForeignKey(DeceasedDetails, on_delete=models.PROTECT, db_column='DeceasedDetailsID')
    contact_details = models.ForeignKey(ContactDetails, on_delete=models.PROTECT, db_column='ContactDetailsID')
    is_primary_contact = models.BooleanField(default=True)
    relationship_type = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='deceased_contact_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='deceased_contact_modified', null=True, blank=True)

    class Meta:
        db_table = 'DeceasedContactMapping'
        unique_together = ['deceased_details', 'contact_details']

    def __str__(self):
        return f"{self.deceased_details} - {self.contact_details}"


class PlotContactMapping(models.Model):
    """Depends on PlotDetails, ContactDetails, User"""
    plot_contact_mapping_id = models.AutoField(primary_key=True)
    plot_details = models.ForeignKey(PlotDetails, on_delete=models.PROTECT, db_column='PlotDetailsID')
    contact_details = models.ForeignKey(ContactDetails, on_delete=models.PROTECT, db_column='ContactDetailsID')
    is_primary_contact = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='plot_contact_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='plot_contact_modified', null=True, blank=True)

    class Meta:
        db_table = 'PlotContactMapping'
        unique_together = ['plot_details', 'contact_details']

    def __str__(self):
        return f"{self.plot_details} - {self.contact_details}"


class MaintenanceDetails(models.Model):
    """Depends on PlotDetails, MaintenanceType, ContactDetails, Notes, User"""
    maintenance_details_id = models.AutoField(primary_key=True)
    plot = models.ForeignKey(PlotDetails, on_delete=models.PROTECT, db_column='PlotID')
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.PROTECT, db_column='MaintenanceTypeID')
    contact_details = models.ForeignKey(ContactDetails, on_delete=models.PROTECT, null=True, blank=True, db_column='ContactDetailsID')
    note = models.ForeignKey(Notes, on_delete=models.PROTECT, null=True, blank=True, db_column='NoteID')
    maintenance_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='maintenance_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='maintenance_modified', null=True, blank=True)

    class Meta:
        db_table = 'MaintenanceDetails'
        indexes = [
            models.Index(fields=['plot', 'maintenance_type'], name='ix_PlotMaintenanceDetails'),
        ]

    def __str__(self):
        return f"{self.plot} - {self.maintenance_type.maintenance_type_constant} - {self.maintenance_date}"


class PaymentStatus(models.Model):
    """Base model - no dependencies"""
    payment_status_id = models.AutoField(primary_key=True)
    payment_status_constant = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payment_status_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payment_status_modified', null=True, blank=True)

    class Meta:
        db_table = 'PaymentStatus'

    def __str__(self):
        return self.payment_status_constant


class PaymentDetails(models.Model):
    """Depends on PlotDetails, DeceasedDetails, ContactDetails, PaymentStatus, Notes, User"""
    payment_details_id = models.AutoField(primary_key=True)
    plot = models.ForeignKey(PlotDetails, on_delete=models.PROTECT, db_column='PlotID')
    deceased_details = models.ForeignKey(DeceasedDetails, on_delete=models.PROTECT, null=True, blank=True, db_column='DeceasedDetailsID')
    contact_details = models.ForeignKey(ContactDetails, on_delete=models.PROTECT, db_column='ContactDetailsID')
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.PROTECT, db_column='PaymentStatusID')
    balance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_paid = models.DateTimeField(null=True, blank=True)
    note = models.ForeignKey(Notes, on_delete=models.PROTECT, null=True, blank=True, db_column='NoteID')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments_created', null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments_modified', null=True, blank=True)

    class Meta:
        db_table = 'PaymentDetails'
        indexes = [
            models.Index(fields=['plot', 'payment_status'], name='ix_PlotPaymentStatus'),
            models.Index(fields=['deceased_details'], name='ix_DeceasedDetails'),
            models.Index(fields=['contact_details'], name='ix_ContactPaymentDetails'),
            models.Index(fields=['date_paid'], name='ix_DatePaid'),
        ]

    def __str__(self):
        return f"Payment {self.payment_details_id} - Plot {self.plot.plot_id}"