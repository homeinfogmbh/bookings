"""Library for renting stuff via digital signage systems."""

from rentallib.email import email
from rentallib.exceptions import RentingError
from rentallib.exceptions import EndBeforeStart
from rentallib.exceptions import DurationTooLong
from rentallib.exceptions import DurationTooShort
from rentallib.exceptions import AlreadyRented
from rentallib.functions import get_rentable, get_renting
from rentallib.orm import Rentable, Renting
from rentallib.wsgi import APPLICATION


__all__ = [
    'APPLICATION',
    'RentingError',
    'EndBeforeStart',
    'DurationTooLong',
    'DurationTooShort',
    'AlreadyRented',
    'get_rentable',
    'get_renting',
    'Rentable',
    'Renting'
]
