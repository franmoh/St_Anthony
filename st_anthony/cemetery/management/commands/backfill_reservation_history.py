"""One-shot backfill: derive a PlotReservationHistory snapshot for every
already-reserved/occupied plot that predates the history table.

Pulls fields from the live ContactDetails / PaymentDetails / Notes rows and
parses the legacy "Witness: X | Signature: Y | Date: Z" blob out of
ContactDetails.note (the pre-history storage for witness/signature).

Idempotent: a plot that already has at least one history row is skipped, so
this can be re-run safely.
"""
import re

from django.core.management.base import BaseCommand
from django.db import transaction

from cemetery.models import (
    PaymentDetails,
    PlotContactMapping,
    PlotDetails,
    PlotReservationHistory,
)


_NOTE_PATTERNS = {
    'witness': r'Witness:\s*(.*?)\s*\|\s*Signature:',
    'signature': r'Signature:\s*(.*?)\s*\|\s*Date:',
}


def _parse_legacy_note(note_text):
    """Returns (witness, signature) from the legacy concatenated note, or (None, None)."""
    if not note_text:
        return None, None
    parsed = {}
    for key, pattern in _NOTE_PATTERNS.items():
        m = re.search(pattern, note_text)
        if m:
            value = m.group(1).strip()
            parsed[key] = None if value == '(none)' else (value or None)
    return parsed.get('witness'), parsed.get('signature')


class Command(BaseCommand):
    help = 'Backfill PlotReservationHistory from existing reservation data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Report what would be written without inserting rows.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        already_have_history = set(
            PlotReservationHistory.objects.values_list('plot_details_id', flat=True)
        )

        candidates = (
            PlotDetails.objects
            .exclude(plot_status=PlotDetails.PlotStatus.AVAILABLE)
            .exclude(pk__in=already_have_history)
        )

        created = 0
        skipped_no_mapping = 0

        for plot in candidates:
            mapping = (
                PlotContactMapping.objects
                .filter(plot_details=plot)
                .select_related('contact_details', 'contact_details__note')
                .order_by('-is_primary_contact', 'created_date')
                .first()
            )
            if mapping is None:
                # Legacy data inconsistency: reserved plot with no contact mapping.
                skipped_no_mapping += 1
                continue

            contact = mapping.contact_details
            note_text = contact.note.note if contact.note_id else None
            witness, signature = _parse_legacy_note(note_text)

            payment = (
                PaymentDetails.objects
                .filter(plot=plot, contact_details=contact)
                .order_by('created_date')
                .first()
            )
            amount_paid = payment.balance_paid if payment else 0

            if dry_run:
                self.stdout.write(
                    f'[dry-run] plot {plot.pk} -> '
                    f'{contact.first_name} {contact.last_name}, ${amount_paid}, '
                    f'witness={witness!r}, signature={signature!r}'
                )
                created += 1
                continue

            with transaction.atomic():
                PlotReservationHistory.objects.create(
                    plot_details=plot,
                    first_name=contact.first_name,
                    middle_name=contact.middle_name,
                    last_name=contact.last_name,
                    address=contact.address,
                    phone_number=contact.phone_number,
                    email=contact.email,
                    amount_paid=amount_paid,
                    reserved_by_name=signature,
                    witness_name=witness,
                    created_date=mapping.created_date,
                    created_by_id=mapping.created_by_id,
                )
            created += 1

        verb = 'Would insert' if dry_run else 'Inserted'
        self.stdout.write(self.style.SUCCESS(
            f'{verb} {created} history row(s); '
            f'{len(already_have_history)} plot(s) already had history; '
            f'{skipped_no_mapping} plot(s) skipped (no contact mapping).'
        ))
