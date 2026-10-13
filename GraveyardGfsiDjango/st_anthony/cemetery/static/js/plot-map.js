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

    // The detail panel scrolls on its own on wide screens: start each newly
    // clicked plot at the top rather than where the last one was left.
    // (detail.elt is the swapped panel here; requestConfig.elt is what was clicked.)
    document.addEventListener('htmx:afterSwap', function (event) {
        const trigger = event.detail.requestConfig && event.detail.requestConfig.elt;
        if (event.detail.target.id === 'plot-detail-panel' && trigger && trigger.closest('.plot-btn')) {
            event.detail.target.scrollTop = 0;
        }
    });
})();

// Top scrollbar: a wide grid ([data-top-scrollbar]) gets a copy of its sideways
// scrollbar above it, kept in step, so it can be scrolled left or right without
// first scrolling down to its bottom edge. Hidden while the grid fits.
(function () {
    function attach(grid) {
        if (grid.dataset.topScrollbarReady) return;
        grid.dataset.topScrollbarReady = 'true';

        const bar = document.createElement('div');
        bar.className = 'plot-top-scrollbar';
        bar.setAttribute('aria-hidden', 'true');
        const spacer = document.createElement('div');
        bar.appendChild(spacer);
        grid.before(bar);

        function resize() {
            spacer.style.width = grid.scrollWidth + 'px';
            bar.hidden = grid.scrollWidth <= grid.clientWidth;
            bar.scrollLeft = grid.scrollLeft;
        }
        // Each side's scroll echoes back once; the equality check stops the loop.
        bar.addEventListener('scroll', function () {
            if (grid.scrollLeft !== bar.scrollLeft) grid.scrollLeft = bar.scrollLeft;
        });
        grid.addEventListener('scroll', function () {
            if (bar.scrollLeft !== grid.scrollLeft) bar.scrollLeft = grid.scrollLeft;
        });
        const observer = new ResizeObserver(resize);
        observer.observe(grid);
        if (grid.firstElementChild) observer.observe(grid.firstElementChild);
        resize();
    }

    htmx.onLoad(function (root) {
        if (root.matches && root.matches('[data-top-scrollbar]')) attach(root);
        root.querySelectorAll('[data-top-scrollbar]').forEach(attach);
    });
})();
