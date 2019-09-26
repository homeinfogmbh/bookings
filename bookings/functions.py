"""Common functions."""

from his import CUSTOMER

from rentallib.messages import NO_SUCH_BOOKABLE, NO_SUCH_BOOKING
from rentallib.orm import Bookable, Booking


__all__ = ['get_bookable', 'get_booking']


def get_bookable(ident):
    """Returns the respective bookable."""

    try:
        return Bookable.get(
            (Bookable.id == ident) & (Bookable.customer == CUSTOMER.id))
    except Bookable.DoesNotExist:
        raise NO_SUCH_BOOKABLE


def get_booking(ident):
    """Returns the respective reservation."""

    try:
        return Booking.select().join(Bookable).where(
            (Booking.id == ident)
            & (Bookable.customer == CUSTOMER.id)
        ).get()
    except Booking.DoesNotExist:
        raise NO_SUCH_BOOKING
