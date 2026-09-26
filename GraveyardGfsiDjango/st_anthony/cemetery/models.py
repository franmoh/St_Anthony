import calendar
import hashlib
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .managers import UsersManager


class BitBooleanField(models.BooleanField):
    """BooleanField for MariaDB bit(1) columns.

    mysqlclient returns bit(1) values as bytes (b'\\x00' / b'\\x01'); both are
    non-empty and therefore truthy in Python, so a vanilla BooleanField evaluates
    to True regardless of the stored bit. This subclass normalizes reads to bool.
    """

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        if isinstance(value, (bytes, bytearray)):
            return value != b'\x00'
        return bool(value)

    def to_python(self, value):
        if isinstance(value, (bytes, bytearray)):
            return value != b'\x00'
        return super().to_python(value)


class Users(AbstractBaseUser):

    class Role(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        BASIC = 'Basic', 'Basic'

    id = models.AutoField(db_column='UserID', primary_key=True)
    password = models.CharField(db_column='Password', max_length=255)
    force_password_change = BitBooleanField(db_column='ForcePasswordChange', default=False)
    is_locked = BitBooleanField(db_column='IsLocked', default=False)
    role = models.CharField(db_column='Role', max_length=50, choices=Role.choices, default=Role.BASIC)
    first_name = models.CharField(db_column='FirstName', max_length=100)
    last_name = models.CharField(db_column='LastName', max_length=100)
    username = models.CharField(db_column='Username', unique=True, max_length=50)
    is_active = models.BooleanField(db_column='IsActive')
    last_login = models.DateField(db_column='LastLogin', blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    created_by = models.ForeignKey('self', models.DO_NOTHING, db_column='CreatedBy')
    modified_date = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True, auto_now=True)
    modified_by = models.ForeignKey('self', models.DO_NOTHING, db_column='ModifiedBy',
                                    related_name='users_modifiedby_set', blank=True, null=True)

    objects = UsersManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def is_staff(self):
        return self.role == self.Role.ADMIN

    @property
    def is_superuser(self):
        return self.role == self.Role.ADMIN

    def has_perm(self, perm, obj=None):
        return self.is_active and self.role == self.Role.ADMIN

    def has_module_perms(self, app_label):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    class Meta:
        managed = False
        db_table = 'Users'


class AuditModel(models.Model):
    created_date = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    created_by = models.ForeignKey(
        'Users',
        models.DO_NOTHING,
        db_column='CreatedBy',
        related_name='%(class)s_created_by'
    )
    modified_date = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True, auto_now=True)
    modified_by = models.ForeignKey(
        'Users',
        models.DO_NOTHING,
        db_column='ModifiedBy',
        related_name='%(class)s_modified_by',
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

class ContactDetails(AuditModel):
    id = models.AutoField(db_column='ContactDetailsID', primary_key=True)
    first_name = models.CharField(db_column='FirstName', max_length=100)
    middle_name = models.CharField(db_column='MiddleName', max_length=100, blank=True, null=True)
    last_name = models.CharField(db_column='LastName', max_length=100)
    phone_number = models.CharField(db_column='PhoneNumber', max_length=100, blank=True, null=True)
    address = models.CharField(db_column='Address', max_length=100, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)
    note = models.ForeignKey('Notes', models.DO_NOTHING, db_column='NoteID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ContactDetails'


class DeceasedContactMapping(AuditModel):
    id = models.AutoField(db_column='DeceasedContactMappingID', primary_key=True)
    deceased_details = models.ForeignKey('DeceasedDetails', models.DO_NOTHING, db_column='DeceasedDetailsID')
    contact_details = models.ForeignKey(ContactDetails, models.DO_NOTHING, db_column='ContactDetailsID')
    is_primary_contact = BitBooleanField(db_column='IsPrimaryContact', default=True)
    relationship_type = models.CharField(db_column='RelationshipType', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DeceasedContactMapping'
        unique_together = (('deceased_details', 'contact_details'),)


class DeceasedDetails(AuditModel):
    id = models.AutoField(db_column='DeceasedDetailsID', primary_key=True)
    plot = models.ForeignKey('PlotDetails', models.DO_NOTHING, db_column='PlotID')
    zone_id = models.IntegerField(db_column='ZoneID', default=0, validators=[MinValueValidator(0), MaxValueValidator(8)])
    deceased_status = models.ForeignKey('DeceasedStatus', models.DO_NOTHING, db_column='DeceasedStatusID')
    first_name = models.CharField(db_column='FirstName', max_length=100, blank=True, null=True)
    last_name = models.CharField(db_column='LastName', max_length=100, blank=True, null=True)
    middle_name = models.CharField(db_column='MiddleName', max_length=100, blank=True, null=True)
    gender = models.CharField(db_column='Gender', max_length=20, blank=True, null=True)
    date_buried = models.DateField(db_column='DateBuried', blank=True, null=True)
    dob_year = models.PositiveSmallIntegerField(db_column='DOBYear', blank=True, null=True)
    dob_month = models.PositiveSmallIntegerField(db_column='DOBMonth', blank=True, null=True)
    dob_day = models.PositiveSmallIntegerField(db_column='DOBDay', blank=True, null=True)
    dod_year = models.PositiveSmallIntegerField(db_column='DODYear', blank=True, null=True)
    dod_month = models.PositiveSmallIntegerField(db_column='DODMonth', blank=True, null=True)
    dod_day = models.PositiveIntegerField(db_column='DODDay', blank=True, null=True)
    note = models.ForeignKey('Notes', models.DO_NOTHING, db_column='NoteID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DeceasedDetails'
        unique_together = (('plot', 'zone_id'),)

    @property
    def dob_iso(self):
        if self.dob_year and self.dob_month and self.dob_day:
            return f'{self.dob_year:04d}-{self.dob_month:02d}-{self.dob_day:02d}'
        return ''

    @property
    def dod_iso(self):
        if self.dod_year and self.dod_month and self.dod_day:
            return f'{self.dod_year:04d}-{self.dod_month:02d}-{self.dod_day:02d}'
        return ''

    @staticmethod
    def _partial_date(year, month, day):
        """'March 4, 1931', 'March 1931' or '1931' depending on what's recorded."""
        if not year:
            return ''
        if month and 1 <= month <= 12:
            month_name = calendar.month_name[month]
            return f'{month_name} {day}, {year}' if day else f'{month_name} {year}'
        return str(year)

    @property
    def dob_display(self):
        return self._partial_date(self.dob_year, self.dob_month, self.dob_day)

    @property
    def dod_display(self):
        return self._partial_date(self.dod_year, self.dod_month, self.dod_day)

    @property
    def lifespan(self):
        """'1931 – 2006', '1931 – ?' or '' when neither year is known."""
        if not (self.dob_year or self.dod_year):
            return ''
        return f"{self.dob_year or '?'} – {self.dod_year or '?'}"

    @property
    def age_at_death(self):
        """Whole years between birth and death; None unless both years are known.
        Month/day refine it when recorded, otherwise it may be one year high."""
        if not (self.dob_year and self.dod_year) or self.dod_year < self.dob_year:
            return None
        age = self.dod_year - self.dob_year
        if self.dob_month and self.dod_month:
            if (self.dod_month, self.dod_day or 0) < (self.dob_month, self.dob_day or 0):
                age -= 1
        return max(age, 0)

    @property
    def primary_contact_mapping(self):
        return (
            self.deceasedcontactmapping_set
            .select_related('contact_details', 'contact_details__note')
            .order_by('-is_primary_contact', 'pk')
            .first()
        )

    @property
    def contact_name(self):
        mapping = self.primary_contact_mapping
        if not mapping or not mapping.contact_details:
            return None
        details = mapping.contact_details
        parts = [details.first_name]
        if details.middle_name:
            parts.append(details.middle_name)
        if details.last_name:
            parts.append(details.last_name)
        return ' '.join(parts)

    @property
    def primary_contact_label(self):
        mapping = self.primary_contact_mapping
        if mapping is None:
            return None
        return 'Yes' if mapping.is_primary_contact else 'No'

    @property
    def contact_relation(self):
        mapping = self.primary_contact_mapping
        return mapping.relationship_type if mapping else None

    @property
    def contact_phone(self):
        mapping = self.primary_contact_mapping
        return mapping.contact_details.phone_number if mapping and mapping.contact_details else None

    @property
    def contact_email(self):
        mapping = self.primary_contact_mapping
        return mapping.contact_details.email if mapping and mapping.contact_details else None

    @property
    def contact_note(self):
        mapping = self.primary_contact_mapping
        if mapping and mapping.contact_details and mapping.contact_details.note:
            return mapping.contact_details.note
        return None

    @property
    def payment(self):
        # Payments are linked to plot + contact, not directly to deceased
        mapping = self.primary_contact_mapping
        if mapping:
            return PaymentDetails.objects.filter(
                plot=self.plot,
                contact_details=mapping.contact_details
            ).select_related('payment_status', 'note').first()
        return None


class DeceasedStatus(AuditModel):
    DISPLAY_NAMES = {
        'FB': 'Full Body',
        'L': 'Living',
        'I': 'Infant',
        'A': 'Ashes',
        'S': 'Spirit',
    }

    id = models.AutoField(db_column='DeceasedStatusID', primary_key=True)
    deceased_status_constant = models.CharField(db_column='DeceasedStatusConstant', unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'DeceasedStatus'

    @property
    def display_name(self):
        return self.DISPLAY_NAMES.get(self.deceased_status_constant, self.deceased_status_constant)


class MaintenanceDetails(AuditModel):
    id = models.AutoField(db_column='MaintenanceDetailsID', primary_key=True)
    plot = models.ForeignKey('PlotDetails', models.DO_NOTHING, db_column='PlotID')
    maintenance_type = models.ForeignKey('MaintenanceType', models.DO_NOTHING, db_column='MaintenanceTypeID')
    contact_details = models.ForeignKey(ContactDetails, models.DO_NOTHING, db_column='ContactDetailsID', blank=True, null=True)
    note = models.ForeignKey('Notes', models.DO_NOTHING, db_column='NoteID', blank=True, null=True)
    maintenance_date = models.DateTimeField(db_column='MaintenanceDate', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MaintenanceDetails'


class MaintenanceStatus(AuditModel):
    id = models.AutoField(db_column='MaintenanceStatusID', primary_key=True)
    maintenance_status_constant = models.CharField(db_column='MaintenanceStatusConstant', unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'MaintenanceStatus'


class MaintenanceType(AuditModel):
    id = models.AutoField(db_column='MaintenanceTypeID', primary_key=True)
    maintenance_type_constant = models.CharField(db_column='MaintenanceTypeConstant', unique=True, max_length=100)
    description = models.CharField(db_column='Description', max_length=255)

    class Meta:
        managed = False
        db_table = 'MaintenanceType'


class Notes(AuditModel):
    id = models.AutoField(db_column='NoteID', primary_key=True)
    note = models.CharField(db_column='Note', max_length=4000)

    class Meta:
        managed = False
        db_table = 'Notes'


class PaymentDetails(AuditModel):
    id = models.AutoField(db_column='PaymentDetailsID', primary_key=True)
    plot = models.ForeignKey('PlotDetails', models.DO_NOTHING, db_column='PlotID')
    deceased_details = models.ForeignKey(DeceasedDetails, models.DO_NOTHING, db_column='DeceasedDetailsID', blank=True, null=True)
    contact_details = models.ForeignKey(ContactDetails, models.DO_NOTHING, db_column='ContactDetailsID')
    payment_status = models.ForeignKey('PaymentStatus', models.DO_NOTHING, db_column='PaymentStatusID')
    balance_paid = models.DecimalField(db_column='BalancePaid', max_digits=10, decimal_places=2, default=0)
    balance_due = models.DecimalField(db_column='BalanceDue', max_digits=10, decimal_places=2, default=0)
    date_paid = models.DateTimeField(db_column='DatePaid', blank=True, null=True)
    note = models.ForeignKey(Notes, models.DO_NOTHING, db_column='NoteID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PaymentDetails'


class PaymentStatus(AuditModel):
    id = models.AutoField(db_column='PaymentStatusID', primary_key=True)
    payment_status_constant = models.CharField(db_column='PaymentStatusConstant', unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'PaymentStatus'


class PlotContactMapping(AuditModel):
    id = models.AutoField(db_column='PlotContactMappingID', primary_key=True)
    plot_details = models.ForeignKey('PlotDetails', models.DO_NOTHING, db_column='PlotDetailsID')
    contact_details = models.ForeignKey(ContactDetails, models.DO_NOTHING, db_column='ContactDetailsID')
    is_primary_contact = BitBooleanField(db_column='IsPrimaryContact', default=True)

    class Meta:
        managed = False
        db_table = 'PlotContactMapping'
        unique_together = (('plot_details', 'contact_details'),)


class PlotReservationHistory(models.Model):
    """Frozen snapshot written at reservation time so reprints are unaffected
    by later edits to ContactDetails / PaymentDetails / Notes. Not an AuditModel
    — the schema only carries CreatedDate/CreatedBy; the row is never modified."""

    id = models.AutoField(db_column='PlotReservationHistoryID', primary_key=True)
    plot_details = models.ForeignKey(
        'PlotDetails', models.DO_NOTHING, db_column='PlotDetailsID',
        related_name='reservation_history',
    )
    cert_number = models.CharField(db_column='CertNumber', max_length=50, blank=True, null=True)
    first_name = models.CharField(db_column='FirstName', max_length=100, blank=True, null=True)
    middle_name = models.CharField(db_column='MiddleName', max_length=100, blank=True, null=True)
    last_name = models.CharField(db_column='LastName', max_length=100, blank=True, null=True)
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)
    phone_number = models.CharField(db_column='PhoneNumber', max_length=100, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)
    amount_paid = models.DecimalField(db_column='AmountPaid', max_digits=10, decimal_places=2, default=0)
    reserved_by_name = models.CharField(db_column='ReservedByName', max_length=200, blank=True, null=True)
    witness_name = models.CharField(db_column='WitnessName', max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(db_column='CreatedDate')
    created_by = models.ForeignKey(
        'Users', models.DO_NOTHING, db_column='CreatedBy',
        related_name='reservation_history_created_by',
    )

    class Meta:
        managed = False
        db_table = 'PlotReservationHistory'


class PlotDetails(AuditModel):

    class PlotStatus(models.TextChoices):
        AVAILABLE = 'Available'
        RESERVED = 'Reserved'
        OCCUPIED = 'Occupied'
        UNKNOWN = 'Unknown'

    id = models.AutoField(db_column='PlotDetailsID', primary_key=True)
    plot_id = models.IntegerField(db_column='PlotID')
    section = models.ForeignKey('Section', models.DO_NOTHING, db_column='SectionID')
    row = models.CharField(db_column='Row', max_length=100, blank=True, null=True)
    unit = models.CharField(db_column='Unit', max_length=100, blank=True, null=True)
    side = models.CharField(db_column='Side', max_length=100, blank=True, null=True)
    niche = models.CharField(db_column='Niche', max_length=100, blank=True, null=True)
    maintenance_status = models.ForeignKey(MaintenanceStatus, models.DO_NOTHING, db_column='MaintenanceStatusID')
    plot_status = models.CharField(db_column='PlotStatus', max_length=9, choices=PlotStatus.choices, default=PlotStatus.AVAILABLE)
    is_available = BitBooleanField(db_column='IsAvailable', default=True)
    note = models.ForeignKey(Notes, models.DO_NOTHING, db_column='NoteID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PlotDetails'

    @property
    def is_columbarium_niche(self):
        if not self.section_id:
            return False
        name = (self.section.section_constant or '').lower()
        return name.startswith('columbar')


class Section(AuditModel):
    id = models.AutoField(db_column='SectionID', primary_key=True)
    section_constant = models.CharField(db_column='SectionConstant', unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'Section'


class ContactMessage(models.Model):
    """Submission from the public Contact Us form. Django-managed (unlike the
    tables above, which mirror the parish's existing MariaDB schema)."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.first_name} {self.last_name} <{self.email}>'


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.email
