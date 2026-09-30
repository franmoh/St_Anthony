// Plot Map and Manage Plots: status filter checkboxes and plot selection.
// Loaded once per page, outside the htmx-swapped section view.

// Status filter: unchecking a status dims its plots. Hidden statuses live on
// <body data-hide-statuses>, so they survive section tab switches and OOB refreshes.
(function () {
    const body = document.body;
    function getHidden() {
        return new Set((body.dataset.hideStatuses || '').split(/\s+/).filter(Boolean));
    }
    function setHidden(set) {
        if (set.size === 0) {
            delete body.dataset.hideStatuses;
        } else {
            body.dataset.hideStatuses = [...set].join(' ');
        }
    }
    document.addEventListener('change', function (event) {
        const box = event.target.closest('[data-status-filter]');
        if (!box) return;
        const hidden = getHidden();
        if (box.checked) {
            hidden.delete(box.value);
        } else {
            hidden.add(box.value);
        }
        setHidden(hidden);
    });
    htmx.onLoad(function (root) {
        const hidden = getHidden();
        root.querySelectorAll('[data-status-filter]').forEach(function (box) {
            box.checked = !hidden.has(box.value);
        });
    });
})();

// Plot selection: the clicked plot stays highlighted while its details show, and a
// section card with data-selected-plot (?plot=<pk>) selects and opens that plot.
(function () {
    let selectedCellId = null;  // e.g. "plot-grid-1392"

    function select(button) {
        document.querySelectorAll('.plot-btn.is-selected').forEach(function (b) {
            b.classList.remove('is-selected');
            b.removeAttribute('aria-current');
        });
        button.classList.add('is-selected');
        button.setAttribute('aria-current', 'true');
        selectedCellId = button.parentElement.id;
    }

    document.addEventListener('click', function (event) {
        const button = event.target.closest('.plot-btn');
        if (button) select(button);
    });

    htmx.onLoad(function (root) {
        const refreshed = selectedCellId && document.querySelector('#' + selectedCellId + ' .plot-btn:not(.is-selected)');
        if (refreshed) select(refreshed);

        const card = root.querySelector('[data-selected-plot]');
        if (!card) return;
        const button = card.querySelector('#plot-grid-' + card.dataset.selectedPlot + ' .plot-btn');
        delete card.dataset.selectedPlot;
        if (!button) return;
        select(button);
        button.scrollIntoView({block: 'center', inline: 'center'});
        htmx.trigger(button, 'click');
    });
})();
