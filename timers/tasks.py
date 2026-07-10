"""Auction timing jobs.

Closes auctions once their end time has passed. Intended to be triggered by
a scheduled backend job (e.g. a cron entry running the
``close_expired_auctions`` management command).
"""
from django.utils import timezone

from bids.models import Bid


def close_auction(listing):
    """Close ``listing`` if its auction window has ended.

    Marks the listing inactive and returns the winning ``Bid`` (or ``None``
    if there were no bids). Returns ``None`` without any effect if the
    listing is already inactive or hasn't reached its end time yet.
    """
    if not listing.is_active:
        return None
    if listing.ends_at is not None and timezone.now() < listing.ends_at:
        return None

    listing.is_active = False
    listing.save(update_fields=['is_active'])
    return Bid.highest_for(listing)
