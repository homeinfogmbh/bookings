"""Library for booking stuff via digital signage systems."""

from rentallib.email import email
from rentallib.exceptions import BookingError
from rentallib.exceptions import EndBeforeStart
from rentallib.exceptions import DurationTooLong
from rentallib.exceptions import DurationTooShort
from rentallib.exceptions import AlreadyBooked
from rentallib.functions import get_bookable, get_booking
from rentallib.orm import Bookable, Booking
from rentallib.wsgi import APPLICATION


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
