"""HIS microservice to manage bookings."""

from flask import request

from his import admin, authenticated, authorized, Application
from notificationlib import get_wsgi_funcs
from wsgilib import JSON, JSONMessage

from bookings.errors import ERRORS
from bookings.functions import get_bookable
from bookings.functions import get_bookables
from bookings.functions import get_booking
from bookings.functions import get_bookings
from bookings.orm import Bookable, NotificationEmail


__all__ = ["APPLICATION"]


APPLICATION = Application("bookings")
GET_EMAILS, SET_EMAILS = get_wsgi_funcs("bookings", NotificationEmail)


@authenticated
@authorized("bookings")
def list_bookables() -> JSON:
    """Lists bookables."""

    return JSON([bookable.to_json() for bookable in get_bookables()])


@authenticated
@admin
@authorized("bookings")
def add_bookable() -> JSONMessage:
    """Deletes the respective bookable."""

    bookable = Bookable.from_json(request.json)
    bookable.save()
    return JSONMessage("The bookable has been added.", id=bookable.id, status=201)


@authenticated
@admin
@authorized("bookings")
def patch_bookable(ident: int) -> JSONMessage:
    """Deletes the respective bookable."""

    bookable = get_bookable(ident)
    bookable.patch_json(request.json)
    bookable.save()
    return JSONMessage("The bookable has been updated.", status=200)


@authenticated
@admin
@authorized("bookings")
def delete_bookable(ident: int) -> JSONMessage:
    """Deletes the respective bookable."""

    get_bookable(ident).delete_instance()
    return JSONMessage("The bookable has been deleted.", status=200)


@authenticated
@authorized("bookings")
def list_bookings() -> JSON:
    """Lists available bookings."""

    return JSON([booking.to_json() for booking in get_bookings()])


@authenticated
@authorized("bookings")
def patch_booking(ident: int) -> JSONMessage:
    """Patches the respective booking."""

    booking = get_booking(ident)
    booking.patch_json(request.json)
    booking.save()
    return JSONMessage("The booking has been updated.", status=200)


@authenticated
@authorized("bookings")
def delete_booking(ident: int) -> JSONMessage:
    """Deletes the respective booking."""

    get_booking(ident).delete_instance()
    return JSONMessage("The booking has been deleted.", status=200)


APPLICATION.add_routes(
    (
        ("GET", "/bookable", list_bookables),
        ("POST", "/bookable", add_bookable),
        ("PATCH", "/bookable/<int:ident>", patch_bookable),
        ("DELETE", "/bookable/<int:ident>", delete_bookable),
        ("GET", "/bookings", list_bookings),
        ("PATCH", "/bookings/<int:ident>", patch_booking),
        ("DELETE", "/bookings/<int:ident>", delete_booking),
        ("GET", "/email", GET_EMAILS),
        ("POST", "/email", SET_EMAILS),
    )
)


for exception, handler in ERRORS.items():
    APPLICATION.register_error_handler(exception, handler)
