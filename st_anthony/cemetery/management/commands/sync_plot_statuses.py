"""Derive PlotStatus from the people recorded in each plot.

A plot holding anyone who is not Living (L) is Occupied; a plot holding only
Living people (pre-arranged burials) is Reserved. Only plots currently marked
Available are changed, so statuses set by hand are left alone.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef

from cemetery.models import DeceasedDetails, PlotDetails

LIVING = 'L'


def sync_plot_statuses(dry_run=False):
    """Return {'Occupied': n, 'Reserved': n} for the plots changed (or that would be)."""
    people = DeceasedDetails.objects.filter(plot=OuterRef('pk'))
    plots = PlotDetails.objects.filter(plot_status=PlotDetails.PlotStatus.AVAILABLE).annotate(
        has_people=Exists(people),
        has_non_living=Exists(people.exclude(deceased_status__deceased_status_constant=LIVING)),
    )
    occupied = plots.filter(has_non_living=True)
    reserved = plots.filter(has_people=True, has_non_living=False)

    counts = {'Occupied': occupied.count(), 'Reserved': reserved.count()}
    if not dry_run:
        with transaction.atomic():
            # Materialise the ids first: MariaDB can't UPDATE a table it subqueries.
            PlotDetails.objects.filter(pk__in=list(occupied.values_list('pk', flat=True))).update(
                plot_status=PlotDetails.PlotStatus.OCCUPIED, is_available=False,
            )
            PlotDetails.objects.filter(pk__in=list(reserved.values_list('pk', flat=True))).update(
                plot_status=PlotDetails.PlotStatus.RESERVED, is_available=False,
            )
    return counts


class Command(BaseCommand):
    help = "Mark Available plots that contain people as Occupied (or Reserved if everyone is Living)."

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help="Report counts without saving.")

    def handle(self, *args, **opts):
        counts = sync_plot_statuses(dry_run=opts['dry_run'])
        verb = "Would mark" if opts['dry_run'] else "Marked"
        self.stdout.write(self.style.SUCCESS(
            f"{verb} {counts['Occupied']} plots Occupied and {counts['Reserved']} plots Reserved."
        ))
