(function () {
    function setText(container, selector, text) {
        var el = container.querySelector(selector);
        if (el) {
            el.textContent = text;
        }
    }

    function formatBidCount(count) {
        return count === 1 ? '1 bid' : count + ' bids';
    }

    function applyListingState(container, data) {
        setText(container, '[data-current-price]', '$' + data.current_price);
        setText(container, '[data-leading-bidder]', data.highest_bidder || 'No bids yet');
        setText(container, '[data-bid-count]', formatBidCount(data.bid_count));

        var status = container.querySelector('[data-listing-status]');
        if (status) {
            status.textContent = data.is_open ? 'Active' : 'Closed';
            status.classList.toggle('text-bg-success', data.is_open);
            status.classList.toggle('text-bg-secondary', !data.is_open);
        }
    }

    function refreshListing(container) {
        fetch(container.getAttribute('data-live-listing-url'), {
            headers: {
                Accept: 'application/json'
            }
        })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('Listing refresh failed');
                }
                return response.json();
            })
            .then(function (data) {
                applyListingState(container, data);
            })
            .catch(function () {
                // Keep the server-rendered values if a refresh is missed.
            });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var container = document.querySelector('[data-live-listing-url]');
        if (!container) {
            return;
        }
        refreshListing(container);
        setInterval(function () {
            refreshListing(container);
        }, 5000);
    });
})();
