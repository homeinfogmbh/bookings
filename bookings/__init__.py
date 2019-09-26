"""Library for booking stuff via digital signage systems."""

from bookings.email import email
from bookings.exceptions import BookingError
from bookings.exceptions import EndBeforeStart
from bookings.exceptions import DurationTooLong
from bookings.exceptions import DurationTooShort
from bookings.exceptions import AlreadyBooked
from bookings.functions import get_bookable, get_booking
from bookings.orm import Bookable, Booking
from bookings.wsgi import APPLICATION


__all__ = [
    'APPLICATION',
    'BookingError',
    'EndBeforeStart',
    'DurationTooLong',
    'DurationTooShort',
    'AlreadyBooked',
    'get_bookable',
    'get_booking',
    'Bookable',
    'Booking'
]
