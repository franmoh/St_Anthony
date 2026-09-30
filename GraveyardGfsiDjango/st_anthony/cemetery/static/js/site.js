// Site-wide behaviour, loaded by base.html. Kept out of inline <script> tags so the
// Content-Security-Policy can allow scripts from this site only (script-src 'self').

    // Mobile hamburger menu toggle.
    (function () {
        var toggle = document.getElementById('nav-toggle');
        var menu = document.getElementById('nav-menu');
        var iconOpen = document.getElementById('nav-icon-open');
        var iconClose = document.getElementById('nav-icon-close');
        if (!toggle || !menu) return;

        toggle.addEventListener('click', function () {
            var isOpen = menu.classList.toggle('hidden') === false;
            toggle.setAttribute('aria-expanded', String(isOpen));
            iconOpen.classList.toggle('hidden', isOpen);
            iconClose.classList.toggle('hidden', !isOpen);
        });

        // Collapse the menu again if the viewport grows past the mobile breakpoint.
        var mql = window.matchMedia('(min-width: 1024px)');
        mql.addEventListener('change', function (e) {
            if (!e.matches) return;
            menu.classList.add('hidden');
            toggle.setAttribute('aria-expanded', 'false');
            iconOpen.classList.remove('hidden');
            iconClose.classList.add('hidden');
        });
    })();

    // Confirm only when moving a plot/niche from Reserved -> Occupied.
    // Scoped to the plot status form so other saves (e.g. maintenance) aren't prompted.
    document.body.addEventListener('htmx:confirm', function (evt) {
        var form = evt.detail.elt;
        if (!form || !form.matches('[data-plot-status-form]')) return;

        var select = form.querySelector('select[name="plot_status"]');
        if (!select) return;  // occupied plots render status read-only (no select)

        if (form.getAttribute('data-current-status') === 'Reserved' && select.value === 'Occupied') {
            evt.preventDefault();  // stop htmx from issuing immediately
            if (window.confirm('Mark this plot as Occupied? This is permanent — once occupied, the status can not be changed back to Reserved or Available.')) {
                evt.detail.issueRequest(true);
            }
        }
    });

    // Unsaved-changes warning. Forms tagged with [data-dirty-tracked] flip to
    // dirty on the first input/change. Warn before:
    //   1. an HTMX swap that would replace #plot-detail-panel from outside a tracked form,
    //   2. full-page navigation / tab close (beforeunload).
    document.body.addEventListener('input', function (evt) {
        var form = evt.target.closest && evt.target.closest('[data-dirty-tracked]');
        if (form) form.dataset.dirty = 'true';
    });
    document.body.addEventListener('change', function (evt) {
        var form = evt.target.closest && evt.target.closest('[data-dirty-tracked]');
        if (form) form.dataset.dirty = 'true';
    });
    // Submitting the form IS the save — clear dirty so beforeunload doesn't
    // warn during the navigation that the submit itself triggers.
    document.body.addEventListener('submit', function (evt) {
        var form = evt.target;
        if (form && form.matches && form.matches('[data-dirty-tracked]')) {
            form.dataset.dirty = 'false';
        }
    });

    document.body.addEventListener('htmx:confirm', function (evt) {
        var target = evt.detail.target;
        if (!target || target.id !== 'plot-detail-panel') return;
        // Submitting a tracked form is a save, not an abandonment.
        var trigger = evt.detail.elt;
        if (trigger && trigger.closest && trigger.closest('[data-dirty-tracked]')) return;

        var dirty = document.querySelector('#plot-detail-panel [data-dirty-tracked][data-dirty="true"]');
        if (!dirty) return;
        evt.preventDefault();
        if (window.confirm('You have unsaved changes in this panel. Discard them?')) {
            evt.detail.issueRequest(true);
        }
    });

    window.addEventListener('beforeunload', function (evt) {
        if (document.querySelector('[data-dirty-tracked][data-dirty="true"]')) {
            evt.preventDefault();
            evt.returnValue = '';
        }
    });

// Home page: hide the parish info cards while the search box is in use.
(function () {
    document.body.addEventListener('focusin', function (event) {
        if (event.target.id !== 'search-input') return;
        var cards = document.getElementById('parish-info-cards');
        if (cards) cards.parentElement.classList.add('hidden');
    });
    document.body.addEventListener('focusout', function (event) {
        if (event.target.id !== 'search-input') return;
        var cards = document.getElementById('parish-info-cards');
        if (cards && !event.target.value.trim()) {
            cards.parentElement.classList.remove('hidden');
        }
    });
})();

// Contact payment edit form (swapped in by htmx): choosing PAID zeroes and locks the
// balance due; editing the amount paid recalculates it from the original total.
htmx.onLoad(function (root) {
    const forms = root.matches && root.matches('[data-payment-edit-form]')
        ? [root] : Array.from(root.querySelectorAll('[data-payment-edit-form]'));
    forms.forEach(function (form) {
        if (form.dataset.paymentEditReady) return;
        form.dataset.paymentEditReady = 'true';
        const paid = form.querySelector('[name="balance_paid"]');
        const due = form.querySelector('[name="balance_due"]');
        const status = form.querySelector('[name="payment_status"]');
        if (!paid || !due || !status) return;

        const total = (parseFloat(paid.value) || 0) + (parseFloat(due.value) || 0);

        function isPaidSelected() {
            const opt = status.options[status.selectedIndex];
            return opt && opt.dataset.constant === 'PAID';
        }

        function syncDueLock() {
            if (isPaidSelected()) {
                due.value = '0.00';
                due.readOnly = true;
                due.classList.add('bg-gray-100', 'text-gray-500', 'cursor-not-allowed');
            } else {
                due.readOnly = false;
                due.classList.remove('bg-gray-100', 'text-gray-500', 'cursor-not-allowed');
            }
        }

        paid.addEventListener('input', () => {
            if (isPaidSelected()) return;
            const p = parseFloat(paid.value) || 0;
            due.value = Math.max(0, total - p).toFixed(2);
        });
        status.addEventListener('change', syncDueLock);
        syncDueLock();
    });
});

// "Back to search" links: return to the previous page (e.g. the same search results)
// when it was on this site; otherwise the link's href is followed.
document.addEventListener('click', function (event) {
    const link = event.target.closest && event.target.closest('[data-back-link]');
    if (!link) return;
    if (document.referrer.indexOf(location.origin) === 0 && history.length > 1) {
        event.preventDefault();
        history.back();
    }
});

// Print buttons (e.g. the reservation certificate).
document.addEventListener('click', function (event) {
    if (event.target.closest && event.target.closest('[data-print]')) window.print();
});
