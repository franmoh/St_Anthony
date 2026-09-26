from decimal import Decimal

from django.core.management.base import BaseCommand

from cemetery.models import PaymentDetails


class Command(BaseCommand):
    help = (
        "Zero balance_due on PaymentDetails rows where payment_status='PAID'. "
        "Fixes data written before the form mirror-bug was patched."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report rows that would change without writing.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        stale = PaymentDetails.objects.filter(
            payment_status__payment_status_constant="PAID"
        ).exclude(balance_due=Decimal("0"))

        count = stale.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS("No stale PAID rows found."))
            return

        self.stdout.write(f"Found {count} PAID rows with non-zero balance_due.")
        if dry_run:
            for p in stale[:20]:
                self.stdout.write(
                    f"  pk={p.pk} plot={p.plot_id} paid={p.balance_paid} due={p.balance_due}"
                )
            if count > 20:
                self.stdout.write(f"  ... and {count - 20} more")
            self.stdout.write("(dry run; no changes written)")
            return

        updated = stale.update(balance_due=Decimal("0"))
        self.stdout.write(self.style.SUCCESS(f"Zeroed balance_due on {updated} rows."))
