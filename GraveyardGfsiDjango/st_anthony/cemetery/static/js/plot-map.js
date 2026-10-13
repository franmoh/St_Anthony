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

// Plot selection and the details pop-up. Clicking a plot loads its details into
// #plot-detail-panel (htmx) inside the #plot-detail-dialog pop-up, which opens on the
// first swap. The × button, a click outside the pop-up or Esc closes it (asking first
// if a form has unsaved changes). A section card with data-selected-plot (?plot=<pk>)
// selects and opens that plot. This script runs before the dialog is parsed, so
// elements are looked up when needed.
(function () {
    let selectedCellId = null;  // e.g. "plot-grid-1392"

    function dialog() { return document.getElementById('plot-detail-dialog'); }
    function panel() { return document.getElementById('plot-detail-panel'); }

    function deselect() {
        document.querySelectorAll('.plot-btn.is-selected').forEach(function (b) {
            b.classList.remove('is-selected');
            b.removeAttribute('aria-current');
        });
    }

    function select(button) {
        deselect();
        button.classList.add('is-selected');
        button.setAttribute('aria-current', 'true');
        selectedCellId = button.parentElement.id;
    }

    function requestClose() {
        const unsaved = panel().querySelector('[data-dirty-tracked][data-dirty="true"]');
        if (unsaved && !window.confirm('You have unsaved changes in this panel. Discard them?')) return;
        dialog().close();
        // Cleared here rather than on the dialog's 'close' event, which fires later
        // (and not at all in a background tab) and could empty a just-reopened pop-up.
        panel().replaceChildren();  // drops any unsaved-form state with it
        deselect();
        selectedCellId = null;
    }

    document.addEventListener('click', function (event) {
        const button = event.target.closest('.plot-btn');
        if (button) select(button);
        if (event.target.closest('[data-close-plot-dialog]')) requestClose();
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

    // Open on the first swap; a newly clicked plot starts at the top of the pop-up.
    // (detail.elt is the swapped panel here; requestConfig.elt is what was clicked.)
    document.addEventListener('htmx:afterSwap', function (event) {
        if (event.detail.target.id !== 'plot-detail-panel') return;
        const trigger = event.detail.requestConfig && event.detail.requestConfig.elt;
        if (trigger && trigger.closest('.plot-btn')) event.detail.target.scrollTop = 0;
        if (!dialog().open) dialog().showModal();
    });

    document.addEventListener('DOMContentLoaded', function () {
        const box = dialog();
        if (!box) return;
        // Esc: same unsaved-changes check as the × button.
        box.addEventListener('cancel', function (event) {
            event.preventDefault();
            requestClose();
        });
        // A click on the backdrop lands on the <dialog> itself (its content fills it).
        // Both press and release must be there, so a drag out of a text box doesn't close it.
        let pressedOutside = false;
        box.addEventListener('mousedown', function (event) {
            pressedOutside = event.target === box;
        });
        box.addEventListener('click', function (event) {
            if (pressedOutside && event.target === box) requestClose();
            pressedOutside = false;
        });
    });
})();

