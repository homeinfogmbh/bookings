"""Common error messages and handlers."""

from wsgilib import JSONMessage

from bookings.exceptions import AlreadyBooked
from bookings.exceptions import DurationTooLong
from bookings.exceptions import DurationTooShort
from bookings.exceptions import EndBeforeStart
from bookings.orm import Bookable, Booking


ERRORS = {
    AlreadyBooked: lambda _: JSONMessage(
        'Bookable is already booked at this time.', status=409),
    Bookable.DoesNotExist: lambda _: JSONMessage(
        'No such bookable.', status=404),
    Booking.DoesNotExist: lambda _: JSONMessage(
        'No such booking.', status=404),
    DurationTooLong: lambda error: JSONMessage(
        'Booking duration is too long.', max_duration=error.max_duration,
        status=400),
    DurationTooShort: lambda error: JSONMessage(
        'Booking duration is too short.', min_duration=error.min_duration,
        status=400),
    EndBeforeStart: lambda _: JSONMessage(
        'Booking ends before it starts.', status=400)
}
