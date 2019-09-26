"""HIS microservice to manage rentables and rents."""

from flask import request

from his import admin, authenticated, authorized, CUSTOMER, Application
from notificationlib import get_wsgi_funcs
from wsgilib import JSON

from bookings.functions import get_bookable, get_booking
from bookings.messages import BOOKABLE_ADDED
from bookings.messages import BOOKABLE_PATCHED
from bookings.messages import BOOKABLE_DELETED
from bookings.messages import BOOKING_PATCHED
from bookings.messages import BOOKING_DELETED
from bookings.orm import Bookable, Booking, NotificationEmail


__all__ = ['APPLICATION']


APPLICATION = Application('bookings')


@authenticated
@authorized('bookings')
def list_bookables():
    """Lists bookables."""

    return JSON([
        bookable.to_json() for bookable in Bookable.select().where(
            Bookable.customer == CUSTOMER.id)])


@authenticated
@admin
@authorized('bookings')
def add_bookable():
    """Deletes the respective bookable."""

    bookable = Bookable.from_json(request.json)
    bookable.save()
    return BOOKABLE_ADDED.update(id=bookable.id)


@authenticated
@admin
@authorized('bookings')
def patch_bookable(ident):
    """Deletes the respective bookable."""

    bookable = get_bookable(ident)
    bookable.patch_json(request.json)
    bookable.save()
    return BOOKABLE_PATCHED


@authenticated
@admin
@authorized('bookings')
def delete_bookable(ident):
    """Deletes the respective bookable."""

    get_bookable(ident).delete_instance()
    return BOOKABLE_DELETED


@authenticated
@authorized('bookings')
def list_bookings():
    """Lists available bookings."""

    return JSON([
        booking.to_json() for booking in Booking.select().join(Bookable).where(
            Bookable.customer == CUSTOMER.id)])


@authenticated
@authorized('bookings')
def patch_booking(ident):
    """Patches the respective booking."""

    booking = get_booking(ident)
    booking.patch_json(request.json)
    booking.save()
    return BOOKING_PATCHED


@authenticated
@authorized('bookings')
def delete_booking(ident):
    """Deletes the respective booking."""

    get_booking(ident).delete_instance()
    return BOOKING_DELETED


GET_EMAILS, SET_EMAILS = get_wsgi_funcs('renting', NotificationEmail)


APPLICATION.add_routes((
    ('GET', '/bookable', list_bookables),
    ('POST', '/bookable', add_bookable),
    ('PATCH', '/bookable/<int:ident>', patch_bookable),
    ('DELETE', '/bookable/<int:ident>', delete_bookable),
    ('GET', '/bookings', list_bookings),
    ('PATCH', '/booking/<int:ident>', patch_booking),
    ('DELETE', '/booking/<int:ident>', delete_booking),
    ('GET', '/email', GET_EMAILS, 'get_emails'),
    ('POST', '/email', SET_EMAILS, 'set_emails')
))
