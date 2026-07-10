(function () {
    function formatRemaining(ms) {
        if (ms <= 0) {
            return 'Auction closed';
        }
        var totalSeconds = Math.floor(ms / 1000);
        var days = Math.floor(totalSeconds / 86400);
        var hours = Math.floor((totalSeconds % 86400) / 3600);
        var minutes = Math.floor((totalSeconds % 3600) / 60);
        var seconds = totalSeconds % 60;
        return days + 'd ' + hours + 'h ' + minutes + 'm ' + seconds + 's';
    }

    function tick() {
        document.querySelectorAll('[data-ends-at]').forEach(function (el) {
            var endsAt = new Date(el.getAttribute('data-ends-at')).getTime();
            var remaining = endsAt - Date.now();
            el.textContent = formatRemaining(remaining);
            el.classList.toggle('text-danger', remaining <= 0);
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        tick();
        setInterval(tick, 1000);
    });
})();
