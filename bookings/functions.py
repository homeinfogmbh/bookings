"""Common functions."""

from his import CUSTOMER

from bookings.messages import NO_SUCH_BOOKABLE, NO_SUCH_BOOKING
from bookings.orm import Bookable, Booking


__all__ = ['get_bookable', 'get_booking']


def get_bookable(ident: int) -> Bookable:
    """Returns the respective bookable."""

    try:
        return Bookable.get(
            (Bookable.id == ident) & (Bookable.customer == CUSTOMER.id))
    except Bookable.DoesNotExist:
        raise NO_SUCH_BOOKABLE from None


def get_booking(ident: int) -> Booking:
    """Returns the respective reservation."""

    try:
        return Booking.select().join(Bookable).where(
            (Booking.id == ident)
            & (Bookable.customer == CUSTOMER.id)
        ).get()
    except Booking.DoesNotExist:
        raise NO_SUCH_BOOKING from None
