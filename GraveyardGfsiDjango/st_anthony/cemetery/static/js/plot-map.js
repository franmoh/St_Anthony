// Plot Map and Manage Plots: status filter checkboxes, grids that fit the screen
// (no sideways scrolling), plot selection and the details pop-up.
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

// Plot grids show only the plots that fit across the screen, with no sideways scrollbar.
// A [data-plot-window] holds one or more [data-window-viewport]s of [data-window-row]s
// (a row label, then .plot-cell cubes) and a [data-window-controls] bar whose ‹ › buttons
// step every row together ("1–12 of 68"). Recounted when the grid's width changes.
const PlotWindow = (function () {
    // .is-first-shown pads 8px on the left instead of 3px (styles.css).
    const FIRST_CELL_EXTRA = 5;

    function rowsOf(win) { return win.querySelectorAll('[data-window-row]'); }
    function cellsOf(row) { return row.querySelectorAll(':scope > .plot-cell'); }

    function maxColumns(win) {
        let max = 0;
        rowsOf(win).forEach(function (row) { max = Math.max(max, cellsOf(row).length); });
        return max;
    }

    // Width of one cube with its gap: a shown cube that isn't first in its row.
    function cellWidth(win) {
        const cell = win.querySelector('[data-window-row] > .plot-cell:not([hidden]) ~ .plot-cell:not([hidden])');
        if (cell) return cell.offsetWidth;
        const button = win.querySelector('.plot-cell:not([hidden]) .plot-btn');
        return button ? button.offsetWidth + 6 : 0;
    }

    function labelWidth(viewport) {
        let width = 0;
        viewport.querySelectorAll('.plot-row-label').forEach(function (label) {
            width = Math.max(width, label.offsetWidth);
        });
        return width;
    }

    function contentWidth(el) {
        const style = getComputedStyle(el);
        return el.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
    }

    // How many cubes fit beside the row labels in the narrowest viewport.
    function fitCount(win) {
        const cube = cellWidth(win);
        if (!cube) return 1;
        let fit = Infinity;
        win.querySelectorAll('[data-window-viewport]').forEach(function (viewport) {
            const room = contentWidth(viewport) - labelWidth(viewport) - FIRST_CELL_EXTRA;
            fit = Math.min(fit, Math.floor(room / cube));
        });
        return fit === Infinity ? 1 : Math.max(1, fit);
    }

    function apply(win) {
        const per = fitCount(win);
        const total = maxColumns(win);
        // Sets step by a screenful (1–5, 6–10, ...); the last one ends on the last plot
        // so it's full width rather than a few cubes beside mostly empty rows.
        const lastStart = Math.max(0, total - per);
        const wanted = Number(win.dataset.windowStart || 0);
        const start = wanted >= lastStart ? lastStart : Math.floor(wanted / per) * per;
        win.dataset.windowStart = start;
        win.dataset.windowPer = per;

        rowsOf(win).forEach(function (row) {
            let first = true;
            cellsOf(row).forEach(function (cell, i) {
                const shown = i >= start && i < start + per;
                cell.hidden = !shown;
                cell.classList.toggle('is-first-shown', shown && first);
                if (shown) first = false;
            });
        });

        const controls = win.querySelector('[data-window-controls]');
        if (!controls) return;
        controls.hidden = total <= per;
        controls.querySelector('[data-window-status]').textContent = controls.dataset.windowNoun + ' ' +
            (start + 1) + '–' + Math.min(start + per, total) + ' of ' + total;
        controls.querySelector('[data-window-prev]').disabled = start === 0;
        controls.querySelector('[data-window-next]').disabled = start >= lastStart;
    }

    function step(win, direction) {
        const per = Number(win.dataset.windowPer) || 1;
        const start = Number(win.dataset.windowStart || 0);
        // Back from the (unaligned) last set returns to the regular steps.
        win.dataset.windowStart = direction > 0
            ? start + per
            : Math.max(0, Math.ceil(start / per) * per - per);
        apply(win);
    }

    // Move a grid so this cube is shown (e.g. a ?plot= deep link).
    function reveal(cell) {
        const win = cell.closest('[data-plot-window]');
        const row = cell.closest('[data-window-row]');
        if (!win || !row) return;
        const index = Array.prototype.indexOf.call(cellsOf(row), cell);
        const per = Number(win.dataset.windowPer) || fitCount(win);
        win.dataset.windowStart = Math.floor(index / per) * per;
        apply(win);
    }

    function init(win) {
        if (win.dataset.windowReady) {
            apply(win);  // e.g. a cube refreshed out of band: keep it within the window
            return;
        }
        win.dataset.windowReady = 'true';
        win.addEventListener('click', function (event) {
            if (event.target.closest('[data-window-prev]')) step(win, -1);
            else if (event.target.closest('[data-window-next]')) step(win, 1);
        });
        let lastWidth = 0;
        new ResizeObserver(function () {
            if (win.clientWidth === lastWidth) return;
            lastWidth = win.clientWidth;
            apply(win);
        }).observe(win);
        apply(win);
    }

    htmx.onLoad(function (root) {
        const around = root.closest && root.closest('[data-plot-window]');
        if (around) init(around);
        root.querySelectorAll('[data-plot-window]').forEach(init);
    });
    // Web fonts can change label widths after the first count.
    window.addEventListener('load', function () {
        document.querySelectorAll('[data-plot-window][data-window-ready]').forEach(apply);
    });

    return {reveal: reveal};
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
        PlotWindow.reveal(button.parentElement);
        button.scrollIntoView({block: 'center', inline: 'nearest'});
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

