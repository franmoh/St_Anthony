import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.template.loader import render_to_string

from .decorators import admin_required, is_admin_user
from .spam_guard import check_submission
from .models import (
    ContactDetails,
    ContactMessage,
    DeceasedContactMapping,
    DeceasedDetails,
    DeceasedStatus,
    MaintenanceDetails,
    MaintenanceStatus,
    NewsletterSubscriber,
    Notes,
    PaymentDetails,
    PaymentStatus,
    PlotContactMapping,
    PlotDetails,
    PlotReservationHistory,
    Section,
)


MAX_MONEY = Decimal('99999999.99')


def _validate_contact_fields(post):
    """Validate contact input. Returns (cleaned_data, errors)."""
    errors = {}
    data = {}

    first_name = (post.get('first_name') or '').strip()
    if not first_name:
        errors['first_name'] = 'First name is required.'
    elif len(first_name) > 100:
        errors['first_name'] = 'First name must be 100 characters or fewer.'
    else:
        data['first_name'] = first_name

    last_name = (post.get('last_name') or '').strip()
    if not last_name:
        errors['last_name'] = 'Last name is required.'
    elif len(last_name) > 100:
        errors['last_name'] = 'Last name must be 100 characters or fewer.'
    else:
        data['last_name'] = last_name

    for field in ('middle_name', 'address', 'phone_number'):
        value = (post.get(field) or '').strip()
        if len(value) > 100:
            errors[field] = f'{field.replace("_", " ").title()} must be 100 characters or fewer.'
        else:
            data[field] = value or None

    email = (post.get('email') or '').strip()
    if email:
        if len(email) > 100:
            errors['email'] = 'Email must be 100 characters or fewer.'
        else:
            try:
                validate_email(email)
                data['email'] = email
            except ValidationError:
                errors['email'] = 'Enter a valid email address.'
    else:
        data['email'] = None

    return data, errors


def _validate_money(raw, field_label):
    """Parse a decimal money value. Returns (value, error)."""
    raw = (raw or '0').strip() or '0'
    try:
        value = Decimal(raw)
    except InvalidOperation:
        return None, f'Enter a valid number for {field_label}.'
    if value < 0:
        return None, f'{field_label} cannot be negative.'
    if value > MAX_MONEY:
        return None, f'{field_label} is too large.'
    if value.as_tuple().exponent < -2:
        return None, f'{field_label} can have at most 2 decimal places.'
    return value, None


def _validate_payment_fields(post, valid_status_ids):
    """Validate payment input. Returns (cleaned_data, errors)."""
    errors = {}
    data = {}

    paid, err = _validate_money(post.get('balance_paid'), 'Amount paid')
    if err:
        errors['balance_paid'] = err
    else:
        data['balance_paid'] = paid

    due, err = _validate_money(post.get('balance_due'), 'Balance due')
    if err:
        errors['balance_due'] = err
    else:
        data['balance_due'] = due

    status_id = (post.get('payment_status') or '').strip()
    if status_id not in valid_status_ids:
        errors['payment_status'] = 'Select a valid payment status.'
    else:
        data['payment_status_id'] = int(status_id)
        # PAID is the terminal state — nothing outstanding by definition.
        if 'balance_due' in data:
            status = PaymentStatus.objects.get(pk=int(status_id))
            if status.payment_status_constant == 'PAID':
                data['balance_due'] = Decimal('0')

    date_paid_raw = (post.get('date_paid') or '').strip()
    if date_paid_raw:
        try:
            data['date_paid'] = datetime.strptime(date_paid_raw, '%Y-%m-%d')
        except ValueError:
            errors['date_paid'] = 'Enter a valid date.'
    else:
        data['date_paid'] = None

    return data, errors


def _validate_deceased_fields(post, valid_status_ids, prefix='deceased_', is_columbarium=False):
    """Validate optional deceased entry. Returns (cleaned_data_or_None, errors).
    Returns (None, {}) if no deceased information was entered.

    Columbarium niches hold up to two ashes; the zone field on the form is
    ignored and the caller assigns zone_id (0 or 1, auto first-free on add,
    preserved on edit).
    """
    errors = {}
    status_id = (post.get(f'{prefix}status') or '').strip()

    other_fields = (
        f'{prefix}first_name', f'{prefix}last_name', f'{prefix}middle_name',
        f'{prefix}gender', f'{prefix}dob', f'{prefix}dod',
        f'{prefix}date_buried',
    )
    any_filled = any((post.get(f) or '').strip() for f in other_fields)

    if not status_id:
        if any_filled:
            errors[f'{prefix}status'] = 'Select a deceased status, or clear the other deceased fields.'
        return None, errors

    if status_id not in valid_status_ids:
        errors[f'{prefix}status'] = 'Select a valid deceased status.'
        return None, errors

    data = {'deceased_status_id': int(status_id)}

    for field, label, required in (
        ('first_name', 'First name', True),
        ('last_name', 'Last name', True),
        ('middle_name', 'Middle name', False),
    ):
        value = (post.get(f'{prefix}{field}') or '').strip()
        if not value and required:
            errors[f'{prefix}{field}'] = f'{label} is required.'
            data[field] = None
        elif len(value) > 100:
            errors[f'{prefix}{field}'] = f'{label} must be 100 characters or fewer.'
        else:
            data[field] = value or None

    gender = (post.get(f'{prefix}gender') or '').strip()
    if len(gender) > 20:
        errors[f'{prefix}gender'] = 'Gender must be 20 characters or fewer.'
    else:
        data['gender'] = gender or None

    parsed_dates = {}
    for form_field, prefix_label in (('dob', 'Date of birth'), ('dod', 'Date of death')):
        raw = (post.get(f'{prefix}{form_field}') or '').strip()
        if raw:
            try:
                parsed = datetime.strptime(raw, '%Y-%m-%d').date()
            except ValueError:
                errors[f'{prefix}{form_field}'] = f'Enter a valid {prefix_label.lower()}.'
                data[f'{form_field}_year'] = None
                data[f'{form_field}_month'] = None
                data[f'{form_field}_day'] = None
                continue
            if parsed.year < 1800 or parsed.year > 2200:
                errors[f'{prefix}{form_field}'] = f'{prefix_label} year must be between 1800 and 2200.'
                data[f'{form_field}_year'] = None
                data[f'{form_field}_month'] = None
                data[f'{form_field}_day'] = None
            else:
                data[f'{form_field}_year'] = parsed.year
                data[f'{form_field}_month'] = parsed.month
                data[f'{form_field}_day'] = parsed.day
                parsed_dates[form_field] = parsed
        else:
            data[f'{form_field}_year'] = None
            data[f'{form_field}_month'] = None
            data[f'{form_field}_day'] = None

    date_buried_raw = (post.get(f'{prefix}date_buried') or '').strip()
    if date_buried_raw:
        try:
            data['date_buried'] = datetime.strptime(date_buried_raw, '%Y-%m-%d').date()
        except ValueError:
            errors[f'{prefix}date_buried'] = 'Enter a valid date.'
    else:
        data['date_buried'] = None

    today = date.today()
    is_living = DeceasedStatus.objects.filter(
        pk=data['deceased_status_id'],
        deceased_status_constant=LIVING_STATUS_CONSTANT,
    ).exists()

    if is_living:
        if 'dod' in parsed_dates:
            errors[f'{prefix}dod'] = 'A living person cannot have a date of death.'
        if data.get('date_buried') is not None:
            errors[f'{prefix}date_buried'] = 'A living person cannot have a date buried.'
    elif 'dod' in parsed_dates and parsed_dates['dod'] > today:
        errors[f'{prefix}dod'] = 'Date of death cannot be in the future.'

    buried = data.get('date_buried')
    if (
        buried is not None
        and 'dod' in parsed_dates
        and buried < parsed_dates['dod']
    ):
        errors[f'{prefix}date_buried'] = 'Date buried cannot be before date of death.'

    if not is_columbarium:
        zone_raw = (post.get(f'{prefix}zone_id') or '0').strip() or '0'
        try:
            zone = int(zone_raw)
            if zone < 0 or zone > 8:
                errors[f'{prefix}zone_id'] = 'Zone must be between 0 and 8.'
            else:
                data['zone_id'] = zone
        except ValueError:
            errors[f'{prefix}zone_id'] = 'Zone must be a number.'

    if errors:
        return None, errors

    return data, errors


FULL_BODY_STATUS_CONSTANT = 'FB'
ASHES_STATUS_CONSTANT = 'A'
LIVING_STATUS_CONSTANT = 'L'


def _get_deceased_statuses_for_plot(plot):
    """Return DeceasedStatus choices filtered by plot type.
    Columbarium niches only allow Ashes; other plots allow all statuses."""
    qs = DeceasedStatus.objects.all().order_by('id')
    if plot.is_columbarium_niche:
        qs = qs.filter(deceased_status_constant=ASHES_STATUS_CONSTANT)
    return list(qs)


def _has_existing_full_body(plot, exclude_pk=None):
    """Return True if plot already has a Full Body deceased (excluding exclude_pk)."""
    qs = DeceasedDetails.objects.filter(
        plot=plot,
        deceased_status__deceased_status_constant=FULL_BODY_STATUS_CONSTANT,
    )
    if exclude_pk is not None:
        qs = qs.exclude(pk=exclude_pk)
    return qs.exists()


def _has_zone_conflict(plot, zone_id, exclude_pk=None):
    """Return True if another DeceasedDetails on this plot already uses zone_id."""
    qs = DeceasedDetails.objects.filter(plot=plot, zone_id=zone_id)
    if exclude_pk is not None:
        qs = qs.exclude(pk=exclude_pk)
    return qs.exists()


def _is_full_body_status_id(deceased_status_id):
    return DeceasedStatus.objects.filter(
        pk=deceased_status_id,
        deceased_status_constant=FULL_BODY_STATUS_CONSTANT,
    ).exists()


def _is_ashes_status_id(deceased_status_id):
    return DeceasedStatus.objects.filter(
        pk=deceased_status_id,
        deceased_status_constant=ASHES_STATUS_CONSTANT,
    ).exists()


def _render_deceased_section(request, plot):
    deceased_list = DeceasedDetails.objects.filter(
        plot=plot
    ).select_related('deceased_status').order_by('zone_id')
    return render(request, 'cemetery/partials/plot_deceased_section_swap.html', {
        'plot': plot,
        'deceased_list': deceased_list,
        'status_choices': PlotDetails.PlotStatus.choices,
    })


def _pending_niche_payment(plot):
    """Niche-specific: the active PARTIAL PaymentDetails row awaiting engraving.
    Returns None for non-niches or when no partial payment exists."""
    if not plot.is_columbarium_niche:
        return None
    return (
        PaymentDetails.objects.filter(plot=plot)
        .select_related('payment_status')
        .filter(payment_status__payment_status_constant='PARTIAL')
        .order_by('-pk')
        .first()
    )


def _latest_reservation_history(plot):
    """Return the newest PlotReservationHistory row for plot, but only if the
    plot has an active reservation (Reserved or Occupied). Cancelled plots
    keep their history for audit, yet have no current cert to reprint."""
    if plot.plot_status not in (
        PlotDetails.PlotStatus.RESERVED,
        PlotDetails.PlotStatus.OCCUPIED,
    ):
        return None
    return (
        PlotReservationHistory.objects
        .filter(plot_details=plot)
        .order_by('-created_date')
        .first()
    )


def _get_contacts_with_payments(plot):
    """Return PlotContactMapping list with each mapping's payment attached as .payment.
    Primary contact is sorted first."""
    contacts = list(
        PlotContactMapping.objects.filter(plot_details=plot)
        .select_related('contact_details', 'contact_details__note')
        .order_by('-is_primary_contact', 'pk')
    )
    for mapping in contacts:
        mapping.payment = (
            PaymentDetails.objects.filter(
                plot=plot, contact_details=mapping.contact_details
            )
            .select_related('payment_status')
            .first()
        )
    return contacts


def _render_contact_section(request, plot):
    return render(request, 'cemetery/partials/plot_contact_section.html', {
        'plot': plot,
        'contacts': _get_contacts_with_payments(plot),
    })


_YEAR_FILTERS = {
    # filter value: (label, year lookup)
    'DOB': ('Year of Birth', 'dob_year'),
    'DOD': ('Year of Death', 'dod_year'),
}
SEARCH_FILTERS = ('', 'Firstname', 'Lastname', *_YEAR_FILTERS)


def normalize_search_filter(filter_type):
    """Unknown or retired filters (e.g. old Year Buried links) fall back to All Fields."""
    return filter_type if filter_type in SEARCH_FILTERS else ''


def _parse_years(query):
    """'1940' -> (1940, 1940); '1940-1950', '1940 1950', '1950 to 1940' -> (1940, 1950).
    Returns None if the query isn't one or two years."""
    parts = [p for p in re.split(r'\s*(?:-|–|to|,|\s)\s*', query.strip(), flags=re.I) if p]
    if not 1 <= len(parts) <= 2 or not all(p.isdigit() and len(p) <= 4 for p in parts):
        return None
    years = [int(p) for p in parts]
    return min(years), max(years)


def _year_q(lookup, years):
    start, end = years
    if start == end:
        return Q(**{lookup: start})
    return Q(**{f'{lookup}__gte': start, f'{lookup}__lte': end})


def _build_search_filters(search_query, filter_type):
    """Returns (filters, search_error). filters is None when the query can't
    produce a valid lookup (e.g. non-numeric year), in which case search_error
    explains why to the user."""
    if filter_type == 'Lastname':
        return Q(last_name__istartswith=search_query), None

    if filter_type == 'Firstname':
        return Q(first_name__istartswith=search_query), None

    if filter_type in _YEAR_FILTERS:
        label, lookup = _YEAR_FILTERS[filter_type]
        years = _parse_years(search_query)
        if years is None:
            return None, f'Please enter a year (e.g. 1940) or a range (e.g. 1940-1950) for {label}.'
        return _year_q(lookup, years), None

    # All fields: numbers are years (one = exact, two or more = range) and
    # everything else is a name. Every name word must start one of the name
    # fields, so "John Doe", "Doe John" and "John A. Doe" all match.
    query = re.sub(r'(\d)\s*(?:-|–|\bto\b)\s*(\d)', r'\1 \2', search_query, flags=re.I)
    tokens = [t.strip('.') for t in re.split(r'[\s,]+', query)]
    tokens = [t for t in tokens if t and t not in ('-', '–')]
    year_tokens = [int(t) for t in tokens if t.isdigit()]
    name_tokens = [t for t in tokens if not t.isdigit()]

    filters = Q()
    if name_tokens:
        name_q = Q()
        for token in name_tokens:
            name_q &= (
                Q(first_name__istartswith=token)
                | Q(middle_name__istartswith=token)
                | Q(last_name__istartswith=token)
            )
        if len(name_tokens) > 1:
            # Compound names stored in one field, e.g. last name "Van Buren".
            whole = ' '.join(name_tokens)
            name_q |= Q(first_name__istartswith=whole) | Q(last_name__istartswith=whole)
        filters &= name_q
    if year_tokens:
        years = (min(year_tokens), max(year_tokens))
        filters &= (
            _year_q('dob_year', years)
            | _year_q('dod_year', years)
            | _year_q('date_buried__year', years)
        )
    if not filters:
        return None, 'Please enter a name or a year to search.'
    return filters, None


SEARCH_RESULTS_PER_PAGE = 10


def home(request):
    search_query = (request.GET.get('search_query') or '').strip()
    filter_type = normalize_search_filter(request.GET.get('filter', ''))
    info = DeceasedDetails.objects.none()
    search_error = None

    if search_query:
        filters, search_error = _build_search_filters(search_query, filter_type)
        if filters is not None:
            info = (
                DeceasedDetails.objects.filter(filters).distinct()
                .order_by('last_name', 'first_name', 'pk')
            )

    page_obj = Paginator(info, SEARCH_RESULTS_PER_PAGE).get_page(request.GET.get('page'))
    context = {
        'info': page_obj.object_list,
        'page_obj': page_obj,
        'page_range': page_obj.paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1),
        'search_error': search_error,
        'search_query': search_query,
        'filter_type': filter_type,
        'search_performed': bool(search_query),
        'no_results_message': f'No records matching your search "{search_query}"',
    }

    if request.headers.get('HX-Request') == 'true':
        results_html = render_to_string('cemetery/partials/search_results.html', context, request=request)
        input_html = render_to_string('cemetery/partials/search_input.html', {
            'filter_type': filter_type,
            'search_query': search_query,
            'oob': True,
        }, request=request)
        return HttpResponse(results_html + input_html)
    return render(request, 'cemetery/home.html', context)

def detail(request):
    deceased_id = request.GET.get('id')
    info = None
    primary_contact = None
    maintenance_details = []

    if deceased_id:
        try:
            info = DeceasedDetails.objects.select_related(
                'plot__section', 'plot__maintenance_status', 'plot__note', 'deceased_status', 'note'
            ).get(id=deceased_id)
            # Fetch maintenance details for the plot
            maintenance_details = MaintenanceDetails.objects.filter(
                plot=info.plot
            ).select_related('maintenance_type', 'contact_details', 'note').order_by('-maintenance_date')
        except (ValueError, DeceasedDetails.DoesNotExist):
            info = None

    payment = None
    # Next-of-kin contacts and payments are private: only admins get them.
    show_private = is_admin_user(request.user)
    if info is not None and show_private:
        mappings = DeceasedContactMapping.objects.select_related(
            'contact_details'
        ).filter(deceased_details=info)
        primary_contact = mappings.filter(is_primary_contact=True).first() or mappings.first()

        payment = (
            PaymentDetails.objects.filter(deceased_details=info)
            .select_related('payment_status', 'note')
            .order_by('-date_paid', '-pk')
            .first()
        )
        if payment is None:
            # Fall back to the plot-level reservation payment (no deceased FK).
            payment = (
                PaymentDetails.objects.filter(plot=info.plot, deceased_details__isnull=True)
                .select_related('payment_status')
                .order_by('-date_paid', '-pk')
                .first()
            )

    return render(request, 'cemetery/detail.html', {
        'info': info,
        'primary_contact': primary_contact,
        'payment': payment,
        'maintenance_details': maintenance_details,
        'show_private': show_private,
    })


_SECTION_STATUS_DISPLAY = [
    (PlotDetails.PlotStatus.AVAILABLE, 'Available', 'bg-emerald-400 border-emerald-600'),
    (PlotDetails.PlotStatus.RESERVED, 'Reserved', 'bg-indigo-400 border-indigo-600'),
    (PlotDetails.PlotStatus.OCCUPIED, 'Occupied', 'bg-amber-400 border-amber-600'),
    (PlotDetails.PlotStatus.UNKNOWN, 'Unknown', 'bg-slate-300 border-slate-500'),
]

_COLUMBARIUM_MONUMENT_ORDER = ['Left', 'Right']


def is_columbarium_section(section):
    if not section or not section.section_constant:
        return False
    name = section.section_constant.lower()
    return name.startswith('columbar')


def _build_columbarium_layout(section_plots):
    """Group columbarium plots by Monument side → Unit → Side → ordered niches.
    Returns [{monument: 'Left', units: [{unit: '30', sides: [{side: 'A', niches: [...]}, ...]}, ...]}, ...]."""
    def niche_sort_key(p):
        try:
            return int(p.niche)
        except (TypeError, ValueError):
            return 10 ** 9

    def unit_sort_key(unit):
        try:
            return int(unit)
        except (TypeError, ValueError):
            return 10 ** 9

    by_monument = {}
    for p in section_plots:
        monument = p.row or ''
        unit = p.unit or ''
        side = p.side or ''
        by_monument.setdefault(monument, {}).setdefault(unit, {}).setdefault(side, []).append(p)

    layout = []
    ordered_monuments = [m for m in _COLUMBARIUM_MONUMENT_ORDER if m in by_monument]
    ordered_monuments += sorted(m for m in by_monument if m not in _COLUMBARIUM_MONUMENT_ORDER)

    for monument in ordered_monuments:
        units = []
        for unit in sorted(by_monument[monument].keys(), key=unit_sort_key):
            sides = []
            for side in sorted(by_monument[monument][unit].keys()):
                niches = sorted(by_monument[monument][unit][side], key=niche_sort_key)
                sides.append({'side': side, 'niches': niches})
            units.append({'unit': unit, 'sides': sides})
        layout.append({'monument': monument, 'units': units})
    return layout


def _status_counts(**filters):
    """{section_id: {plot_status: count}} from a single aggregate query."""
    counts = {}
    rows = (
        PlotDetails.objects.filter(**filters)
        .values_list('section_id', 'plot_status')
        .annotate(n=Count('pk'))
        .order_by()
    )
    for section_id, status, n in rows:
        counts.setdefault(section_id, {})[status] = n
    return counts


def _compute_section_stats(status_counts):
    total = sum(status_counts.values())
    if not total:
        return []
    # Every status is listed (even at 0) because each one doubles as a filter checkbox.
    stats = []
    for status, label, swatch in _SECTION_STATUS_DISPLAY:
        count = status_counts.get(status, 0)
        stats.append({
            'status': status,
            'label': label,
            'swatch': swatch,
            'count': count,
            'pct': round(count * 100 / total),
        })
    return stats


def _set_detail_urls(plots, detail_url_name):
    """Attach p.detail_url using a single reverse() instead of one per button."""
    template = reverse(detail_url_name, kwargs={'pk': 0})
    head, _, tail = template.rpartition('0')
    for p in plots:
        p.detail_url = f'{head}{p.pk}{tail}'


def _build_section_page(request, detail_url_name):
    """Section tabs (counts only) plus the full grid for the one selected
    section. Rendering every section at once meant thousands of buttons."""
    counts = _status_counts()
    tabs = [
        {'section': s, 'total': sum(counts.get(s.id, {}).values())}
        for s in Section.objects.order_by('id')
    ]

    selected = None
    try:
        requested_id = int(request.GET.get('section', ''))
    except ValueError:
        requested_id = None
    # ?plot=<pk> deep-links to one plot: open its section and select it.
    selected_plot_id = None
    plot_param = request.GET.get('plot', '')
    if plot_param.isdigit():
        match = PlotDetails.objects.filter(pk=int(plot_param)).values_list('pk', 'section_id').first()
        if match:
            selected_plot_id, requested_id = match
    if requested_id is not None:
        selected = next((t for t in tabs if t['section'].id == requested_id), None)
    if selected is None:
        selected = next((t for t in tabs if t['total']), tabs[0] if tabs else None)
    if selected is None:
        return tabs, None

    section = selected['section']
    section_plots = list(
        PlotDetails.objects.filter(section=section)
        .only('id', 'plot_id', 'section_id', 'row', 'unit', 'side', 'niche', 'plot_status')
        .order_by('row', 'plot_id')
    )
    _set_detail_urls(section_plots, detail_url_name)
    is_columbarium = is_columbarium_section(section)

    rows = {}
    for p in section_plots:
        rows.setdefault(p.row or '', []).append(p)

    item = {
        'section': section,
        'rows': rows,
        'has_row_labels': any(key != '' for key in rows),
        'total': selected['total'],
        'stats': _compute_section_stats(counts.get(section.id, {})),
        'is_columbarium': is_columbarium,
        'columbarium_layout': _build_columbarium_layout(section_plots) if is_columbarium else None,
        'selected_plot_id': selected_plot_id,
    }
    return tabs, item


def _section_stats_item_for_plot(plot):
    counts = _status_counts(section_id=plot.section_id).get(plot.section_id, {})
    return {'section': plot.section, 'stats': _compute_section_stats(counts)}


def _get_plot_related_data(plot):
    """Fetch deceased and contact details for a plot."""
    deceased_list = DeceasedDetails.objects.filter(
        plot=plot
    ).select_related('deceased_status').order_by('zone_id')

    contacts = PlotContactMapping.objects.filter(
        plot_details=plot
    ).select_related('contact_details')

    return deceased_list, contacts


def _render_plot_map(request, template, detail_url_name):
    tabs, item = _build_section_page(request, detail_url_name)
    context = {'tabs': tabs, 'item': item, 'detail_url_name': detail_url_name}
    if request.headers.get('HX-Request') == 'true':
        # Tab switch: swap just the tabs + selected section.
        template = 'cemetery/partials/plot_section_view.html'
    return render(request, template, context)


# --- Public views ---

def plot(request):
    return _render_plot_map(request, 'cemetery/plot_map.html', 'plot_info')


def plot_info(request, pk):
    plot = get_object_or_404(
        PlotDetails.objects.select_related('section', 'maintenance_status', 'note'),
        pk=pk,
    )
    deceased_list, contacts = _get_plot_related_data(plot)
    # Public map panel: contact details only for admins.
    if not is_admin_user(request.user):
        contacts = contacts.none()

    return render(request, 'cemetery/partials/plot_info.html', {
        'plot': plot,
        'deceased_list': deceased_list,
        'contacts': contacts,
    })


# --- Admin/manage views ---

@admin_required
def manage_plots(request):
    return _render_plot_map(request, 'cemetery/manage_plots.html', 'manage_plot_detail')


@admin_required
def manage_plot_detail(request, pk):
    plot = get_object_or_404(
        PlotDetails.objects.select_related('section', 'maintenance_status', 'note'),
        pk=pk,
    )
    maintenance_statuses = MaintenanceStatus.objects.all()
    deceased_list = DeceasedDetails.objects.filter(
        plot=plot
    ).select_related('deceased_status').order_by('zone_id')
    contacts = _get_contacts_with_payments(plot)

    if request.method == 'POST':
        requested_status = request.POST.get('plot_status', plot.plot_status)
        status_error = None
        if (
            plot.plot_status == PlotDetails.PlotStatus.RESERVED
            and requested_status == PlotDetails.PlotStatus.AVAILABLE
        ):
            status_error = 'Use Cancel Reservation to free a reserved plot.'
        elif (
            plot.plot_status in (
                PlotDetails.PlotStatus.AVAILABLE,
                PlotDetails.PlotStatus.UNKNOWN,
            )
            and requested_status in (
                PlotDetails.PlotStatus.RESERVED,
                PlotDetails.PlotStatus.OCCUPIED,
            )
        ):
            status_error = 'Use Reserve to assign this plot.'
        elif (
            plot.plot_status == PlotDetails.PlotStatus.OCCUPIED
            and requested_status != PlotDetails.PlotStatus.OCCUPIED
        ):
            status_error = 'Occupied plots are final and cannot change status.'
        elif (
            plot.plot_status == PlotDetails.PlotStatus.RESERVED
            and requested_status == PlotDetails.PlotStatus.OCCUPIED
            and not deceased_list.exists()
        ):
            status_error = 'Add at least one deceased record before marking this plot as Occupied.'
        else:
            plot.plot_status = requested_status
            plot.is_available = plot.plot_status == PlotDetails.PlotStatus.AVAILABLE

        maintenance_status_id = request.POST.get('maintenance_status')
        if maintenance_status_id:
            plot.maintenance_status_id = int(maintenance_status_id)
        
        # Handle plot note
        note_text = (request.POST.get('plot_note') or '').strip()
        if note_text:
            if plot.note:
                # Update existing note
                plot.note.note = note_text
                plot.note.modified_by_id = 1
                plot.note.save()
            else:
                # Create new note
                note = Notes.objects.create(
                    note=note_text,
                    created_by_id=1,
                )
                plot.note = note
        elif plot.note and not note_text:
            # User cleared the note
            plot.note = None
        
        plot.save()

        return render(request, 'cemetery/partials/plot_detail_with_grid_swap.html', {
            'plot': plot,
            'maintenance_statuses': maintenance_statuses,
            'status_choices': PlotDetails.PlotStatus.choices,
            'deceased_list': deceased_list,
            'contacts': contacts,
            'latest_history': _latest_reservation_history(plot),
            'pending_niche_payment': _pending_niche_payment(plot),
            'saved': not status_error,
            'status_error': status_error,
            'section_stats_item': _section_stats_item_for_plot(plot),
        })

    return render(request, 'cemetery/partials/plot_detail.html', {
        'plot': plot,
        'maintenance_statuses': maintenance_statuses,
        'status_choices': PlotDetails.PlotStatus.choices,
        'deceased_list': deceased_list,
        'contacts': contacts,
        'latest_history': _latest_reservation_history(plot),
        'pending_niche_payment': _pending_niche_payment(plot),
    })


@admin_required
def cancel_reservation(request, pk):
    plot = get_object_or_404(PlotDetails, pk=pk)

    if request.method != 'POST':
        return redirect('manage_plot_detail', pk=pk)

    if plot.plot_status != PlotDetails.PlotStatus.RESERVED:
        return redirect('manage_plot_detail', pk=pk)

    with transaction.atomic():
        # TODO(auth): replace created/modified placeholders with request.user once login is wired up.
        PaymentDetails.objects.filter(plot=plot).delete()

        # DeceasedContactMapping has FKs into both DeceasedDetails and
        # ContactDetails. Models use DO_NOTHING so we must clear it manually
        # before deleting either side, or MariaDB rejects the delete.
        deceased_ids = list(
            DeceasedDetails.objects.filter(plot=plot).values_list('pk', flat=True)
        )
        if deceased_ids:
            DeceasedContactMapping.objects.filter(
                deceased_details_id__in=deceased_ids
            ).delete()
        DeceasedDetails.objects.filter(plot=plot).delete()

        contact_ids = list(
            PlotContactMapping.objects.filter(plot_details=plot)
            .values_list('contact_details_id', flat=True)
        )
        PlotContactMapping.objects.filter(plot_details=plot).delete()

        # Only delete a ContactDetails if no other mapping (plot, deceased, or
        # maintenance) still references it.
        for cid in contact_ids:
            still_referenced = (
                PlotContactMapping.objects.filter(contact_details_id=cid).exists()
                or DeceasedContactMapping.objects.filter(contact_details_id=cid).exists()
                or MaintenanceDetails.objects.filter(contact_details_id=cid).exists()
            )
            if not still_referenced:
                ContactDetails.objects.filter(pk=cid).delete()

        plot.plot_status = PlotDetails.PlotStatus.AVAILABLE
        plot.is_available = True
        plot.save()

    plot = PlotDetails.objects.select_related('section', 'maintenance_status', 'note').get(pk=pk)
    maintenance_statuses = MaintenanceStatus.objects.all()
    deceased_list = DeceasedDetails.objects.filter(
        plot=plot
    ).select_related('deceased_status').order_by('zone_id')
    contacts = _get_contacts_with_payments(plot)

    return render(request, 'cemetery/partials/plot_detail_with_grid_swap.html', {
        'plot': plot,
        'maintenance_statuses': maintenance_statuses,
        'status_choices': PlotDetails.PlotStatus.choices,
        'deceased_list': deceased_list,
        'contacts': contacts,
        'latest_history': _latest_reservation_history(plot),
        'saved': True,
        'section_stats_item': _section_stats_item_for_plot(plot),
    })


@admin_required
def reserve_plot(request, pk):
    plot = get_object_or_404(
        PlotDetails.objects.select_related('section', 'maintenance_status'),
        pk=pk,
    )

    if plot.plot_status != PlotDetails.PlotStatus.AVAILABLE:
        return redirect('manage_plots')

    deceased_statuses = _get_deceased_statuses_for_plot(plot)
    valid_status_ids = {str(s.pk) for s in deceased_statuses}

    if request.method == 'POST':
        data, errors = _validate_contact_fields(request.POST)
        witness = (request.POST.get('witness') or '').strip()[:500]
        signature = (request.POST.get('signature') or '').strip()[:500]
        date_of_raw = (request.POST.get('date_of') or '').strip()

        is_niche = plot.is_columbarium_niche

        if is_niche:
            deposit, deposit_err = _validate_money(request.POST.get('deposit'), 'Deposit')
            total, total_err = _validate_money(request.POST.get('total'), 'Total price')
            if deposit_err:
                errors['deposit'] = deposit_err
            elif deposit is None or deposit <= 0:
                errors['deposit'] = 'Deposit must be greater than zero.'
            if total_err:
                errors['total'] = total_err
            elif total is None or total <= 0:
                errors['total'] = 'Total price must be greater than zero.'
            if 'deposit' not in errors and 'total' not in errors and deposit > total:
                errors['deposit'] = 'Deposit cannot exceed total price.'
            amount = deposit
        else:
            amount, amount_err = _validate_money(request.POST.get('amount'), 'Amount')
            if amount_err:
                errors['amount'] = amount_err
            elif amount is None or amount <= 0:
                errors['amount'] = 'Reservation requires payment greater than zero.'
            total = amount

        date_paid = None
        if date_of_raw:
            try:
                date_paid = datetime.strptime(date_of_raw, '%Y-%m-%d')
            except ValueError:
                errors['date_of'] = 'Enter a valid date.'

        deceased_data, deceased_errors = _validate_deceased_fields(
            request.POST, valid_status_ids, is_columbarium=plot.is_columbarium_niche,
        )
        errors.update(deceased_errors)

        if errors:
            return render(request, 'cemetery/reserve_plot.html', {
                'plot': plot,
                'today': date.today(),
                'errors': errors,
                'form_data': request.POST,
                'deceased_statuses': deceased_statuses,
            })

        if date_paid is None:
            date_paid = datetime.combine(date.today(), datetime.min.time())

        with transaction.atomic():
            # TODO(auth): replace created_by_id=1 with request.user.id once login is wired up.
            contact = ContactDetails.objects.create(
                created_by_id=1,
                **data,
            )

            PlotContactMapping.objects.create(
                plot_details=plot,
                contact_details=contact,
                is_primary_contact=True,
                created_by_id=1,
            )

            if is_niche:
                payment_status_const = 'PARTIAL'
                balance_paid = amount
                balance_due = total - amount
                payment_date_paid = date_paid if balance_due == 0 else None
            else:
                payment_status_const = 'PAID'
                balance_paid = amount
                balance_due = Decimal('0')
                payment_date_paid = date_paid

            payment = PaymentDetails.objects.create(
                plot=plot,
                contact_details=contact,
                payment_status=PaymentStatus.objects.get(payment_status_constant=payment_status_const),
                balance_paid=balance_paid,
                balance_due=balance_due,
                date_paid=payment_date_paid,
                created_by_id=1,
            )

            history = PlotReservationHistory.objects.create(
                plot_details=plot,
                # TODO(Q5): cert_number is null until the team's numbering scheme lands.
                first_name=data.get('first_name'),
                middle_name=data.get('middle_name'),
                last_name=data.get('last_name'),
                address=data.get('address'),
                phone_number=data.get('phone_number'),
                email=data.get('email'),
                amount_paid=amount,
                reserved_by_name=signature or None,
                witness_name=witness or None,
                created_date=datetime.now(),
                created_by_id=1,
            )

            if deceased_data is not None:
                deceased = DeceasedDetails.objects.create(
                    plot=plot,
                    created_by_id=1,
                    **deceased_data,
                )
                # Link the deceased to the reservation's contact and payment so the
                # public detail page (which filters by deceased_details) finds them.
                DeceasedContactMapping.objects.create(
                    deceased_details=deceased,
                    contact_details=contact,
                    is_primary_contact=True,
                    created_by_id=1,
                )

            plot.plot_status = PlotDetails.PlotStatus.RESERVED
            plot.is_available = False
            plot.save()

        url = reverse('reservation_certificate', kwargs={'pk': plot.pk, 'history_pk': history.pk})
        return redirect(f'{url}?fresh=1')

    return render(request, 'cemetery/reserve_plot.html', {
        'plot': plot,
        'today': date.today(),
        'deceased_statuses': deceased_statuses,
    })


@admin_required
def mark_engraving_complete(request, pk):
    plot = get_object_or_404(
        PlotDetails.objects.select_related('section', 'maintenance_status', 'note'),
        pk=pk,
    )

    if request.method != 'POST':
        return redirect('manage_plot_detail', pk=plot.pk)

    payment = _pending_niche_payment(plot)
    if payment is not None:
        with transaction.atomic():
            payment.balance_paid = payment.balance_paid + payment.balance_due
            payment.balance_due = Decimal('0')
            payment.payment_status = PaymentStatus.objects.get(payment_status_constant='PAID')
            payment.date_paid = datetime.now()
            payment.save()

    maintenance_statuses = MaintenanceStatus.objects.all()
    deceased_list = DeceasedDetails.objects.filter(
        plot=plot
    ).select_related('deceased_status').order_by('zone_id')
    return render(request, 'cemetery/partials/plot_detail.html', {
        'plot': plot,
        'maintenance_statuses': maintenance_statuses,
        'status_choices': PlotDetails.PlotStatus.choices,
        'deceased_list': deceased_list,
        'contacts': _get_contacts_with_payments(plot),
        'latest_history': _latest_reservation_history(plot),
        'pending_niche_payment': _pending_niche_payment(plot),
        'saved': payment is not None,
    })


@admin_required
def reservation_certificate(request, pk, history_pk):
    plot = get_object_or_404(
        PlotDetails.objects.select_related('section'),
        pk=pk,
    )
    history = get_object_or_404(
        PlotReservationHistory,
        pk=history_pk,
        plot_details=plot,
    )
    return render(request, 'cemetery/reservation_certificate.html', {
        'plot': plot,
        'history': history,
    })


def _render_contact_card(request, mapping):
    """Render the expanded contact card body + an OOB swap for the summary badge."""
    mapping.payment = (
        PaymentDetails.objects.filter(
            plot=mapping.plot_details, contact_details=mapping.contact_details
        )
        .select_related('payment_status')
        .first()
    )
    return render(request, 'cemetery/partials/plot_contact_card_swap.html', {
        'c': mapping,
        'plot': mapping.plot_details,
        'pending_niche_payment': _pending_niche_payment(mapping.plot_details),
    })


@admin_required
def plot_contact_card(request, mapping_pk):
    mapping = get_object_or_404(
        PlotContactMapping.objects.select_related('contact_details', 'plot_details'),
        pk=mapping_pk,
    )
    return _render_contact_card(request, mapping)


@admin_required
def edit_plot_contact(request, mapping_pk):
    mapping = get_object_or_404(
        PlotContactMapping.objects.select_related('contact_details', 'contact_details__note', 'plot_details'),
        pk=mapping_pk,
    )
    contact = mapping.contact_details

    if request.method == 'POST':
        data, errors = _validate_contact_fields(request.POST)
        if errors:
            return render(request, 'cemetery/partials/plot_contact_edit.html', {
                'c': mapping,
                'errors': errors,
                'form_data': request.POST,
            })

        with transaction.atomic():
            for field, value in data.items():
                setattr(contact, field, value)
            
            # Handle contact note
            note_text = (request.POST.get('contact_note') or '').strip()
            if note_text:
                if contact.note:
                    # Update existing note
                    contact.note.note = note_text
                    contact.note.modified_by_id = 1
                    contact.note.save()
                else:
                    # Create new note
                    note = Notes.objects.create(
                        note=note_text,
                        created_by_id=1,
                    )
                    contact.note = note
            elif contact.note and not note_text:
                # User cleared the note
                contact.note = None
            
            # TODO(auth): replace with request.user.id once login is wired up.
            contact.modified_by_id = 1
            contact.save()

        return _render_contact_card(request, mapping)

    return render(request, 'cemetery/partials/plot_contact_edit.html', {
        'c': mapping,
    })


@admin_required
def edit_plot_contact_payment(request, mapping_pk):
    mapping = get_object_or_404(
        PlotContactMapping.objects.select_related('contact_details', 'plot_details'),
        pk=mapping_pk,
    )
    payment = (
        PaymentDetails.objects.filter(
            plot=mapping.plot_details, contact_details=mapping.contact_details
        )
        .select_related('payment_status')
        .first()
    )
    payment_statuses = list(PaymentStatus.objects.all())
    valid_status_ids = {str(s.pk) for s in payment_statuses}

    if request.method == 'POST':
        data, errors = _validate_payment_fields(request.POST, valid_status_ids)
        if errors:
            return render(request, 'cemetery/partials/plot_contact_payment_edit.html', {
                'c': mapping,
                'payment': payment,
                'payment_statuses': payment_statuses,
                'errors': errors,
                'form_data': request.POST,
            })

        with transaction.atomic():
            # TODO(auth): replace created_by_id / modified_by_id with request.user.id.
            if payment:
                for field, value in data.items():
                    setattr(payment, field, value)
                payment.modified_by_id = 1
                payment.save()
            else:
                PaymentDetails.objects.create(
                    plot=mapping.plot_details,
                    contact_details=mapping.contact_details,
                    created_by_id=1,
                    **data,
                )

        return _render_contact_card(request, mapping)

    return render(request, 'cemetery/partials/plot_contact_payment_edit.html', {
        'c': mapping,
        'payment': payment,
        'payment_statuses': payment_statuses,
    })


@admin_required
def add_contact(request, pk):
    plot = get_object_or_404(PlotDetails, pk=pk)

    if plot.plot_status == PlotDetails.PlotStatus.AVAILABLE:
        response = _render_contact_section(request, plot)
        response['HX-Retarget'] = '#contact-section'
        response['HX-Reswap'] = 'outerHTML'
        return response

    if request.method == 'POST':
        data, errors = _validate_contact_fields(request.POST)
        if errors:
            return render(request, 'cemetery/partials/plot_contact_add.html', {
                'plot': plot,
                'errors': errors,
                'form_data': request.POST,
            })

        set_primary = request.POST.get('set_primary') == 'on'

        with transaction.atomic():
            # TODO(auth): replace created_by_id=1 with request.user.id once login is wired up.
            contact = ContactDetails.objects.create(
                created_by_id=1,
                **data,
            )
            deceased_list = DeceasedDetails.objects.filter(plot=plot)
            if set_primary:
                PlotContactMapping.objects.filter(
                    plot_details=plot, is_primary_contact=True
                ).update(is_primary_contact=False, modified_by_id=1)
                DeceasedContactMapping.objects.filter(
                    deceased_details__in=deceased_list, is_primary_contact=True
                ).update(is_primary_contact=False, modified_by_id=1)
            PlotContactMapping.objects.create(
                plot_details=plot,
                contact_details=contact,
                is_primary_contact=set_primary,
                created_by_id=1,
            )

            # Link contact to all deceased on this plot via DeceasedContactMapping
            for deceased in deceased_list:
                DeceasedContactMapping.objects.create(
                    deceased_details=deceased,
                    contact_details=contact,
                    is_primary_contact=set_primary,
                    created_by_id=1,
                )

        response = _render_contact_section(request, plot)
        response['HX-Retarget'] = '#contact-section'
        response['HX-Reswap'] = 'outerHTML'
        return response

    return render(request, 'cemetery/partials/plot_contact_add.html', {
        'plot': plot,
    })


@admin_required
def cancel_add_contact(request, pk):
    plot = get_object_or_404(PlotDetails, pk=pk)
    return render(request, 'cemetery/partials/plot_contact_add_button.html', {
        'plot': plot,
    })


@admin_required
def make_primary_contact(request, mapping_pk):
    mapping = get_object_or_404(
        PlotContactMapping.objects.select_related('plot_details'),
        pk=mapping_pk,
    )
    if request.method != 'POST':
        return _render_contact_section(request, mapping.plot_details)

    if not mapping.is_primary_contact:
        with transaction.atomic():
            # TODO(auth): replace modified_by_id=1 with request.user.id once login is wired up.
            PlotContactMapping.objects.filter(
                plot_details=mapping.plot_details, is_primary_contact=True
            ).update(is_primary_contact=False, modified_by_id=1)
            DeceasedContactMapping.objects.filter(
                contact_details=mapping.contact_details, is_primary_contact=True
            ).update(is_primary_contact=False, modified_by_id=1)
            mapping.is_primary_contact = True
            mapping.modified_by_id = 1
            mapping.save()
            DeceasedContactMapping.objects.filter(
                contact_details=mapping.contact_details
            ).update(is_primary_contact=True, modified_by_id=1)

    return _render_contact_section(request, mapping.plot_details)


@admin_required
def delete_contact(request, mapping_pk):
    mapping = get_object_or_404(
        PlotContactMapping.objects.select_related('plot_details', 'contact_details'),
        pk=mapping_pk,
    )
    plot = mapping.plot_details

    if request.method != 'POST' or mapping.is_primary_contact:
        return _render_contact_section(request, plot)

    contact = mapping.contact_details
    with transaction.atomic():
        PaymentDetails.objects.filter(
            plot=plot, contact_details=contact
        ).delete()
        DeceasedContactMapping.objects.filter(
            contact_details=contact
        ).delete()
        mapping.delete()
        # Orphan check: if this contact has no other plot/deceased/maintenance links, delete it.
        still_referenced = (
            PlotContactMapping.objects.filter(contact_details=contact).exists()
            or DeceasedContactMapping.objects.filter(contact_details=contact).exists()
            or MaintenanceDetails.objects.filter(contact_details=contact).exists()
        )
        if not still_referenced:
            contact.delete()

    return _render_contact_section(request, plot)


@admin_required
def add_deceased(request, pk):
    plot = get_object_or_404(PlotDetails, pk=pk)

    if plot.plot_status == PlotDetails.PlotStatus.AVAILABLE:
        response = _render_deceased_section(request, plot)
        response['HX-Retarget'] = '#deceased-section'
        response['HX-Reswap'] = 'outerHTML'
        return response

    deceased_statuses = _get_deceased_statuses_for_plot(plot)
    valid_status_ids = {str(s.pk) for s in deceased_statuses}

    if request.method == 'POST':
        data, errors = _validate_deceased_fields(
            request.POST, valid_status_ids, is_columbarium=plot.is_columbarium_niche,
        )
        if data is None and not errors:
            errors['deceased_status'] = 'Status is required.'

        if not errors:
            if data['deceased_status_id'] and _is_full_body_status_id(data['deceased_status_id']):
                if _has_existing_full_body(plot):
                    errors['deceased_status'] = 'This plot already has a Full Body deceased recorded.'
            if not plot.is_columbarium_niche and 'zone_id' in data:
                is_ashes = _is_ashes_status_id(data['deceased_status_id'])
                if is_ashes and data['zone_id'] == 0:
                    errors['deceased_zone_id'] = 'Ashes cannot use zone 0 (reserved for body burial). Use zones 1–8.'
                elif not is_ashes and data['zone_id'] != 0:
                    errors['deceased_zone_id'] = 'Non-ashes (Full Body, Living, Infant, Spirit) must be in zone 0.'
                elif _has_zone_conflict(plot, data['zone_id']):
                    errors['deceased_zone_id'] = f'Zone {data["zone_id"]} is already used on this plot.'
            if plot.is_columbarium_niche:
                used_zones = set(
                    DeceasedDetails.objects.filter(plot=plot).values_list('zone_id', flat=True)
                )
                if 0 not in used_zones:
                    data['zone_id'] = 0
                elif 1 not in used_zones:
                    data['zone_id'] = 1
                else:
                    errors['deceased_status'] = 'This niche is full (max 2 ashes).'

        if errors:
            return render(request, 'cemetery/partials/plot_deceased_add.html', {
                'plot': plot,
                'deceased_statuses': deceased_statuses,
                'errors': errors,
                'form_data': request.POST,
            })

        # TODO(auth): replace created_by_id=1 with request.user.id once login is wired up.
        with transaction.atomic():
            deceased = DeceasedDetails.objects.create(
                plot=plot,
                created_by_id=1,
                **data,
            )
            # Link the new deceased to the plot's primary contact so the public
            # detail page populates Contact Details / Payment Status. Falls back
            # to the first mapping if no row is flagged primary.
            primary_mapping = (
                PlotContactMapping.objects
                .filter(plot_details=plot)
                .order_by('-is_primary_contact', 'pk')
                .first()
            )
            if primary_mapping is not None:
                DeceasedContactMapping.objects.create(
                    deceased_details=deceased,
                    contact_details=primary_mapping.contact_details,
                    is_primary_contact=True,
                    created_by_id=1,
                )

        response = _render_deceased_section(request, plot)
        # Form's default hx-target is #deceased-add-region; on success we want the
        # whole section to refresh so the new card appears.
        response['HX-Retarget'] = '#deceased-section'
        response['HX-Reswap'] = 'outerHTML'
        return response

    return render(request, 'cemetery/partials/plot_deceased_add.html', {
        'plot': plot,
        'deceased_statuses': deceased_statuses,
    })


@admin_required
def cancel_add_deceased(request, pk):
    plot = get_object_or_404(PlotDetails, pk=pk)
    return render(request, 'cemetery/partials/plot_deceased_add_button.html', {
        'plot': plot,
    })


@admin_required
def deceased_card(request, pk):
    d = get_object_or_404(
        DeceasedDetails.objects.select_related('deceased_status'),
        pk=pk,
    )
    return render(request, 'cemetery/partials/plot_deceased_card.html', {'d': d})


@admin_required
def edit_deceased(request, pk):
    d = get_object_or_404(
        DeceasedDetails.objects.select_related('deceased_status', 'plot'),
        pk=pk,
    )
    plot = d.plot
    deceased_statuses = _get_deceased_statuses_for_plot(plot)
    valid_status_ids = {str(s.pk) for s in deceased_statuses}

    if request.method == 'POST':
        data, errors = _validate_deceased_fields(
            request.POST, valid_status_ids, is_columbarium=plot.is_columbarium_niche,
        )
        if data is None and not errors:
            errors['deceased_status'] = 'Status is required.'

        if not errors:
            if data['deceased_status_id'] and _is_full_body_status_id(data['deceased_status_id']):
                if _has_existing_full_body(plot, exclude_pk=d.pk):
                    errors['deceased_status'] = 'This plot already has a Full Body deceased recorded.'
            if not plot.is_columbarium_niche and 'zone_id' in data:
                is_ashes = _is_ashes_status_id(data['deceased_status_id'])
                if is_ashes and data['zone_id'] == 0:
                    errors['deceased_zone_id'] = 'Ashes cannot use zone 0 (reserved for body burial). Use zones 1–8.'
                elif not is_ashes and data['zone_id'] != 0:
                    errors['deceased_zone_id'] = 'Non-ashes (Full Body, Living, Infant, Spirit) must be in zone 0.'
                elif _has_zone_conflict(plot, data['zone_id'], exclude_pk=d.pk):
                    errors['deceased_zone_id'] = f'Zone {data["zone_id"]} is already used on this plot.'
            if plot.is_columbarium_niche:
                data['zone_id'] = d.zone_id

        if errors:
            return render(request, 'cemetery/partials/plot_deceased_edit.html', {
                'd': d,
                'deceased_statuses': deceased_statuses,
                'errors': errors,
                'form_data': request.POST,
            })

        for field, value in data.items():
            setattr(d, field, value)
        # TODO(auth): replace with request.user.id once login is wired up.
        d.modified_by_id = 1
        d.save()

        d = DeceasedDetails.objects.select_related('deceased_status').get(pk=d.pk)
        return render(request, 'cemetery/partials/plot_deceased_card_swap.html', {'d': d})

    return render(request, 'cemetery/partials/plot_deceased_edit.html', {
        'd': d,
        'deceased_statuses': deceased_statuses,
    })


@admin_required
def delete_deceased(request, pk):
    d = get_object_or_404(DeceasedDetails.objects.select_related('plot'), pk=pk)
    plot = d.plot

    if request.method != 'POST':
        return redirect('manage_plot_detail', pk=plot.pk)

    with transaction.atomic():
        # Clear DeceasedContactMapping rows pointing at this deceased before
        # deleting it (models use DO_NOTHING, so MariaDB would otherwise reject).
        DeceasedContactMapping.objects.filter(deceased_details=d).delete()
        # PaymentDetails has a nullable deceased_details FK; unlink any rows
        # that still point at this deceased so the delete doesn't fail.
        PaymentDetails.objects.filter(deceased_details=d).update(deceased_details=None)
        d.delete()
    return _render_deceased_section(request, plot)


def deceased_note_section(request, pk):
    """Public read of the deceased note panel on the search detail page.
    Edit/delete buttons inside the partial are template-gated to authenticated users."""
    deceased = get_object_or_404(DeceasedDetails.objects.select_related('note'), pk=pk)
    return render(request, 'cemetery/partials/deceased_note_section.html', {'deceased': deceased})


@login_required
def edit_deceased_note(request, pk):
    deceased = get_object_or_404(DeceasedDetails.objects.select_related('note'), pk=pk)

    if request.method == 'POST':
        text = (request.POST.get('note') or '').strip()
        errors = {}
        if not text:
            errors['note'] = 'Note cannot be empty.'
        elif len(text) > 4000:
            errors['note'] = 'Note must be 4000 characters or fewer.'

        if errors:
            return render(request, 'cemetery/partials/deceased_note_edit.html', {
                'deceased': deceased,
                'errors': errors,
                'form_data': request.POST,
            })

        with transaction.atomic():
            if deceased.note_id:
                note_obj = deceased.note
                note_obj.note = text
                note_obj.modified_by_id = request.user.id
                note_obj.save()
            else:
                note_obj = Notes.objects.create(note=text, created_by_id=request.user.id)
                deceased.note = note_obj
                deceased.modified_by_id = request.user.id
                deceased.save(update_fields=['note', 'modified_by', 'modified_date'])

        deceased = DeceasedDetails.objects.select_related('note').get(pk=deceased.pk)
        return render(request, 'cemetery/partials/deceased_note_section.html', {'deceased': deceased})

    return render(request, 'cemetery/partials/deceased_note_edit.html', {'deceased': deceased})


@login_required
def delete_deceased_note(request, pk):
    deceased = get_object_or_404(DeceasedDetails.objects.select_related('note'), pk=pk)

    if request.method != 'POST':
        return redirect(f"{reverse('detail')}?id={deceased.pk}")

    if deceased.note_id:
        note_obj = deceased.note
        with transaction.atomic():
            deceased.note = None
            deceased.modified_by_id = request.user.id
            deceased.save(update_fields=['note', 'modified_by', 'modified_date'])
            note_obj.delete()

    deceased = DeceasedDetails.objects.select_related('note').get(pk=deceased.pk)
    return render(request, 'cemetery/partials/deceased_note_section.html', {'deceased': deceased})


@admin_required
def note_section(request, pk):
    plot = get_object_or_404(PlotDetails.objects.select_related('note'), pk=pk)
    return render(request, 'cemetery/partials/plot_note_section.html', {'plot': plot})


@admin_required
def edit_note(request, pk):
    plot = get_object_or_404(PlotDetails.objects.select_related('note'), pk=pk)

    if request.method == 'POST':
        text = (request.POST.get('note') or '').strip()
        errors = {}
        if not text:
            errors['note'] = 'Note cannot be empty.'
        elif len(text) > 4000:
            errors['note'] = 'Note must be 4000 characters or fewer.'

        if errors:
            return render(request, 'cemetery/partials/plot_note_edit.html', {
                'plot': plot,
                'errors': errors,
                'form_data': request.POST,
            })

        with transaction.atomic():
            # TODO(auth): replace created_by_id / modified_by_id with request.user.id once login is wired up.
            if plot.note_id:
                note_obj = plot.note
                note_obj.note = text
                note_obj.modified_by_id = 1
                note_obj.save()
            else:
                note_obj = Notes.objects.create(note=text, created_by_id=1)
                plot.note = note_obj
                plot.modified_by_id = 1
                plot.save(update_fields=['note', 'modified_by', 'modified_date'])

        plot = PlotDetails.objects.select_related('note').get(pk=plot.pk)
        return render(request, 'cemetery/partials/plot_note_section.html', {'plot': plot})

    return render(request, 'cemetery/partials/plot_note_edit.html', {'plot': plot})


@admin_required
def delete_note(request, pk):
    plot = get_object_or_404(PlotDetails.objects.select_related('note'), pk=pk)

    if request.method != 'POST':
        return redirect('manage_plot_detail', pk=plot.pk)

    if plot.note_id:
        note_obj = plot.note
        with transaction.atomic():
            # TODO(auth): replace modified_by_id with request.user.id once login is wired up.
            plot.note = None
            plot.modified_by_id = 1
            plot.save(update_fields=['note', 'modified_by', 'modified_date'])
            note_obj.delete()

    plot = PlotDetails.objects.select_related('note').get(pk=plot.pk)
    return render(request, 'cemetery/partials/plot_note_section.html', {'plot': plot})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    username = ""
    next_url = request.GET.get("next", "")
    login_error = ""

    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        next_url = request.POST.get("next", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Only follow ?next= back into this site; anything else would be an open redirect.
            if not url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                next_url = ''
            return redirect(next_url or "home")

        login_error = "Invalid username or password."

    return render(
        request,
        "cemetery/login.html",
        {
            "username": username,
            "next": next_url,
            "login_error": login_error,
        },
    )


@require_POST
def logout_view(request):
    auth_logout(request)
    return redirect("home")


def about(request):
    return render(request, 'cemetery/about.html')


def contact(request):
    return render(request, 'cemetery/contact.html')


def _validate_contact_message_fields(post):
    """Validate the public Contact Us form. Returns (cleaned_data, errors)."""
    errors = {}
    data = {}

    first_name = (post.get('first_name') or '').strip()
    if not first_name:
        errors['first_name'] = 'First name is required.'
    elif len(first_name) > 100:
        errors['first_name'] = 'First name must be 100 characters or fewer.'
    else:
        data['first_name'] = first_name

    last_name = (post.get('last_name') or '').strip()
    if not last_name:
        errors['last_name'] = 'Last name is required.'
    elif len(last_name) > 100:
        errors['last_name'] = 'Last name must be 100 characters or fewer.'
    else:
        data['last_name'] = last_name

    email = (post.get('email') or '').strip()
    if not email:
        errors['email'] = 'Email is required.'
    elif len(email) > 254:
        errors['email'] = 'Email must be 254 characters or fewer.'
    else:
        try:
            validate_email(email)
            data['email'] = email
        except ValidationError:
            errors['email'] = 'Enter a valid email address.'

    phone = (post.get('phone') or '').strip()
    if len(phone) > 30:
        errors['phone'] = 'Phone must be 30 characters or fewer.'
    else:
        data['phone'] = phone

    message = (post.get('message') or '').strip()
    if not message:
        errors['message'] = 'Please enter a message.'
    elif len(message) > 4000:
        errors['message'] = 'Message must be 4000 characters or fewer.'
    else:
        data['message'] = message

    return data, errors


@require_POST
def contact_submit(request):
    verdict = check_submission(request.POST)
    if verdict == 'bot':
        # Look successful so the bot moves on; nothing is saved or emailed.
        return render(request, 'cemetery/partials/contact_form.html', {'sent': True})
    if verdict == 'expired':
        return render(request, 'cemetery/partials/contact_form.html', {
            'errors': {'form': 'This form expired. Please check your message and send it again.'},
            'form_data': request.POST,
        })

    data, errors = _validate_contact_message_fields(request.POST)
    if errors:
        return render(request, 'cemetery/partials/contact_form.html', {
            'errors': errors,
            'form_data': request.POST,
        })

    ContactMessage.objects.create(**data)

    if settings.CONTACT_FORM_RECIPIENT_EMAIL:
        send_mail(
            subject=f"New contact form message from {data['first_name']} {data['last_name']}",
            message=(
                f"From: {data['first_name']} {data['last_name']} <{data['email']}>\n"
                f"Phone: {data['phone'] or 'n/a'}\n\n{data['message']}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_FORM_RECIPIENT_EMAIL],
            fail_silently=True,
        )

    return render(request, 'cemetery/partials/contact_form.html', {'sent': True})


@require_POST
def newsletter_subscribe(request):
    email = (request.POST.get('email') or '').strip()
    error = None

    verdict = check_submission(request.POST)
    if verdict == 'bot':
        # Look successful so the bot moves on; nothing is saved.
        return render(request, 'cemetery/partials/newsletter_form.html', {'subscribed': True})
    if verdict == 'expired':
        error = 'This form expired. Please try again.'
    elif not email:
        error = 'Email is required.'
    else:
        try:
            validate_email(email)
        except ValidationError:
            error = 'Enter a valid email address.'

    if error:
        return render(request, 'cemetery/partials/newsletter_form.html', {'error': error, 'email': email})

    NewsletterSubscriber.objects.get_or_create(email=email)
    return render(request, 'cemetery/partials/newsletter_form.html', {'subscribed': True})
