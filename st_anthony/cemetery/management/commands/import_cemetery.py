"""Python port of the cemetery_importer_v1 Perl importer (import_cemetery.pl).

Loads plots and deceased records from the cleaned master CSV. Contacts, payments
and notes are not inserted; rows that need them are written to the issue log
instead, as in the original.

Deliberate differences from the Perl script:
- "$Balance Due" is read. The Perl looked for a "Balance Due" header that the
  CSV doesn't have, so its payment check only ever saw "Paid In Full".
- Section C matches "Columbarium" or the Perl's "Columnbarium" spelling,
  whichever the database has seeded.
- PlotReservationHistory is also cleared by --reset (it references PlotDetails).
- Plot statuses are derived from the imported people afterwards
  (see sync_plot_statuses); the Perl left every plot Available.
"""
import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from django.db.models import Max

from cemetery.models import (
    DeceasedDetails,
    DeceasedStatus,
    MaintenanceStatus,
    PlotDetails,
    Section,
    Users,
)

from .sync_plot_statuses import sync_plot_statuses

# CSV section code -> accepted SectionConstant spellings, first match wins.
SECTION_MAP = {
    'W': ('Western',),
    'M': ('Middle',),
    'U': ('Upper',),
    'L': ('Lower',),
    'C': ('Columbarium', 'Columnbarium'),
    'P': ('Paul',),
}

# Children before parents: the FKs are enforced by MariaDB, not Django (DO_NOTHING).
RESET_TABLES = [
    'DeceasedContactMapping',
    'PlotContactMapping',
    'PaymentDetails',
    'MaintenanceDetails',
    'PlotReservationHistory',
    'DeceasedDetails',
    'PlotDetails',
    'ContactDetails',
    'Notes',
]

CSV_COLUMNS = {
    'section': 'Section',
    'row': 'Row',
    'plot': 'Plot',
    'unit': 'Unit',
    'side': 'Side',
    'niche': 'Niche',
    'status': 'Status',
    'last_name': 'Last Name',
    'first_name': 'First Name',
    'initial': 'Initial',
    'birth_death_year': 'Birth/ Death Year',
    'birth_year': 'Birth Year',
    'birth_month': 'Birth Month',
    'birth_day': 'Birth Day',
    'death_year': 'Death Year',
    'death_month': 'Death Month',
    'death_day': 'Death Day',
    'paid_in_full': 'Paid In Full',
    'balance_due': '$Balance Due',
    'note': 'Note',
}

INT_FIELDS = ('plot', 'birth_year', 'birth_month', 'birth_day', 'death_year', 'death_month', 'death_day')
DECEASED_FIELDS = ('last_name', 'first_name', 'initial', 'birth_year', 'death_year', 'status', 'birth_death_year')
LOCATION_FIELDS = ('section', 'row', 'plot', 'unit', 'side', 'niche')
MAX_ZONE = 8

LOG_HEADER = ['source_line', 'severity', 'section', 'row', 'plot', 'unit', 'side', 'niche', 'name', 'issue', 'action']


def _clean(value):
    if value is None:
        return None
    value = value.strip()
    return value or None


def read_rows(path):
    """Yield one dict per non-blank CSV record, keyed by CSV_COLUMNS names."""
    with open(path, newline='', encoding='utf-8-sig') as fh:
        reader = csv.reader(fh)
        header = [h.strip() for h in next(reader)]
        index = {name: i for i, name in enumerate(header)}
        line = 1
        for record in reader:
            line += 1
            if not any(v.strip() for v in record):
                continue

            row = {'source_line': line}
            for field, column in CSV_COLUMNS.items():
                i = index.get(column)
                row[field] = _clean(record[i]) if i is not None and i < len(record) else None

            row['has_location'] = row['section'] is not None and any(
                row[f] is not None for f in ('plot', 'unit', 'niche')
            )
            # Evaluated before PROBLEM years are blanked, matching the Perl importer.
            row['has_deceased_data'] = any(row[f] is not None for f in DECEASED_FIELDS)

            for year in ('birth_year', 'death_year'):
                problem = row[year] is not None and row[year].lower() == 'problem'
                row[f'problem_{year}'] = problem
                if problem:
                    row[year] = None

            for field in INT_FIELDS:
                if row[field] is None:
                    continue
                try:
                    row[field] = int(row[field])
                except ValueError:
                    raise CommandError(
                        f"CSV line {line}: {CSV_COLUMNS[field]} is not a number: {row[field]!r}"
                    )
            yield row


class IssueLog:
    def __init__(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = open(path, 'w', newline='', encoding='utf-8')
        self._writer = csv.writer(self._fh, lineterminator='\n')  # same line endings as the Perl log
        self._writer.writerow(LOG_HEADER)
        self.count = 0

    def issue(self, row, issue, action, severity='WARNING'):
        name = ' '.join(n for n in (row['first_name'], row['last_name']) if n)
        self._writer.writerow([
            row['source_line'], severity,
            *(row[f] for f in LOCATION_FIELDS),
            name, issue, action,
        ])
        self.count += 1

    def close(self):
        self._fh.close()


class Command(BaseCommand):
    help = "Import plots and deceased records from the cleaned cemetery master CSV."

    def add_arguments(self, parser):
        parser.add_argument('--csv', required=True, help="Path to the cleaned master CSV.")
        parser.add_argument('--dry-run', action='store_true',
                            help="Validate and log issues without writing to the database.")
        parser.add_argument('--reset', action='store_true',
                            help="Delete existing plot/deceased/contact/payment/note data first. Back up first.")
        parser.add_argument('--default-status', default='FB',
                            help="DeceasedStatus constant for rows with no status (default: FB).")
        parser.add_argument('--maintenance-status', default='GOOD',
                            help="MaintenanceStatus constant for new plots (default: GOOD).")
        parser.add_argument('--import-user-id', type=int, default=1,
                            help="Users.UserID recorded as CreatedBy/ModifiedBy (default: 1).")
        parser.add_argument('--log', help="Issue log path (default: logs/import_errors.csv next to the CSV).")

    def handle(self, *args, **opts):
        csv_path = Path(opts['csv'])
        if not csv_path.is_file():
            raise CommandError(f"CSV not found: {csv_path}")
        log_path = Path(opts['log']) if opts['log'] else csv_path.parent / 'logs' / 'import_errors.csv'
        dry_run = opts['dry_run']
        self.user_id = opts['import_user_id']

        if not Users.objects.filter(pk=self.user_id).exists():
            raise CommandError(f"Import user {self.user_id} does not exist.")

        # Keyed case-insensitively, like the Perl's SQL lookups under MySQL's default collation.
        self.sections = {s.section_constant.lower(): s.pk for s in Section.objects.all()}
        self.statuses = {s.deceased_status_constant.upper(): s.pk for s in DeceasedStatus.objects.all()}
        self.default_status = opts['default_status'].upper()
        if self.default_status not in self.statuses:
            raise CommandError(f"Default deceased status '{self.default_status}' not found.")
        maint = MaintenanceStatus.objects.filter(maintenance_status_constant=opts['maintenance_status']).first()
        if maint is None:
            raise CommandError(f"Maintenance status '{opts['maintenance_status']}' not found.")
        self.maintenance_status_id = maint.pk

        self.stats = {'rows': 0, 'plots_created': 0, 'plots_matched': 0, 'deceased': 0, 'skipped': 0}
        self.dry_run_zones = {}
        self.dry_run_plots = set()
        self.log = IssueLog(log_path)

        try:
            with transaction.atomic():
                if opts['reset'] and not dry_run:
                    self._reset()
                for row in read_rows(csv_path):
                    self._process(row, dry_run)
                if dry_run:
                    transaction.set_rollback(True)
                else:
                    self.status_counts = sync_plot_statuses()
        except CommandError:
            raise
        except Exception as e:
            raise CommandError(f"Import failed; transaction rolled back.\n{e}") from e
        finally:
            self.log.close()

        s = self.stats
        verb = "Dry run completed. No changes committed." if dry_run else "Import completed successfully."
        self.stdout.write(self.style.SUCCESS(verb))
        self.stdout.write(
            f"Rows processed: {s['rows']} | skipped (no location): {s['skipped']} | "
            f"plots created: {s['plots_created']} | plots matched existing: {s['plots_matched']} | "
            f"deceased {'to create' if dry_run else 'created'}: {s['deceased']}"
        )
        if not dry_run:
            self.stdout.write(
                f"Plot statuses set: {self.status_counts['Occupied']} Occupied, "
                f"{self.status_counts['Reserved']} Reserved"
            )
        self.stdout.write(f"Issues logged: {self.log.count} -> {log_path}")

    def _reset(self):
        with connection.cursor() as cursor:
            for table in RESET_TABLES:
                cursor.execute(f"DELETE FROM `{table}`")

    def _process(self, row, dry_run):
        self.stats['rows'] += 1

        if not row['has_location']:
            self.stats['skipped'] += 1
            self.log.issue(row, 'Record has no cemetery location', 'Skipped and flagged for review')
            return

        plot = self._find_or_create_plot(row, dry_run)

        if not row['has_deceased_data']:
            self.log.issue(row, 'Plot/location has no deceased/contact information in CSV',
                           'Flagged; no fabricated contact inserted')
            return

        self._create_deceased(row, plot, dry_run)
        self.log.issue(row, 'CSV contains no contact information for this plot',
                       'Flagged; no fabricated contact inserted')
        if row['paid_in_full'] is not None or row['balance_due'] is not None:
            self.log.issue(row, 'Payment data present but contact information is unavailable',
                           'Payment not inserted; flagged for review')

    def _find_or_create_plot(self, row, dry_run):
        names = SECTION_MAP.get(row['section'])
        if names is None:
            raise CommandError(f"CSV line {row['source_line']}: unknown section code '{row['section']}'")
        section_id = next((self.sections[n.lower()] for n in names if n.lower() in self.sections), None)
        if section_id is None:
            raise CommandError(f"Section '{' / '.join(names)}' does not exist in the database")

        plot_id = row['plot']
        if plot_id is None and all(row[f] is not None for f in ('unit', 'side', 'niche')):
            plot_id = 0

        lookup = {
            'section_id': section_id,
            'row': row['row'],
            'plot_id': plot_id,
            'unit': row['unit'],
            'side': row['side'],
            'niche': row['niche'],
        }
        existing = PlotDetails.objects.filter(**lookup).first()
        key = tuple(lookup.values())
        if existing or key in self.dry_run_plots:
            self.stats['plots_matched'] += 1
            return existing

        self.stats['plots_created'] += 1
        if dry_run:
            self.dry_run_plots.add(key)
            return None
        return PlotDetails.objects.create(
            **lookup,
            maintenance_status_id=self.maintenance_status_id,
            created_by_id=self.user_id,
            modified_by_id=self.user_id,
        )

    def _create_deceased(self, row, plot, dry_run):
        code = (row['status'] or self.default_status).upper()
        status_id = self.statuses.get(code)
        if status_id is None:
            raise CommandError(f"CSV line {row['source_line']}: deceased status '{code}' not found")

        if row['problem_birth_year'] or row['problem_death_year']:
            self.log.issue(row, 'Problem value in birth/death year', 'Stored corresponding year as NULL')

        self.stats['deceased'] += 1

        if dry_run:
            key = tuple(row[f] for f in LOCATION_FIELDS)
            zone = self.dry_run_zones.get(key, 0)
            self.dry_run_zones[key] = zone + 1
            if zone > MAX_ZONE:
                raise CommandError(f"Plot {key} has exhausted ZoneID 0-{MAX_ZONE}")
            return

        current = DeceasedDetails.objects.filter(plot=plot).aggregate(m=Max('zone_id'))['m']
        zone = 0 if current is None else current + 1
        if zone > MAX_ZONE:
            raise CommandError(f"Plot {plot.pk} has exhausted ZoneID 0-{MAX_ZONE}")

        DeceasedDetails.objects.create(
            plot=plot,
            zone_id=zone,
            deceased_status_id=status_id,
            first_name=row['first_name'],
            last_name=row['last_name'],
            middle_name=row['initial'],
            dob_year=row['birth_year'],
            dob_month=row['birth_month'],
            dob_day=row['birth_day'],
            dod_year=row['death_year'],
            dod_month=row['death_month'],
            dod_day=row['death_day'],
            created_by_id=self.user_id,
            modified_by_id=self.user_id,
        )
