"""Common messages."""

from wsgilib import JSONMessage


__all__ = [
    'NO_SUCH_BOOKABLE',
    'BOOKABLE_ADDED',
    'BOOKABLE_PATCHED',
    'BOOKABLE_DELETED',
    'NO_SUCH_BOOKING',
    'BOOKING_PATCHED',
    'BOOKING_DELETED'
]


NO_SUCH_BOOKABLE = JSONMessage('No such BOOKABLE.', status=404)
BOOKABLE_ADDED = JSONMessage('The bookable has been added.', status=201)
BOOKABLE_PATCHED = JSONMessage('The bookable has been updated.', status=200)
BOOKABLE_DELETED = JSONMessage('The bookable has been deleted.', status=200)
NO_SUCH_BOOKING = JSONMessage('No such booking.', status=404)
BOOKING_PATCHED = JSONMessage('The booking has been updated.', status=200)
BOOKING_DELETED = JSONMessage('The booking has been deleted.', status=200)
