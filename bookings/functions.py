"""Common functions."""

from peewee import ModelSelect

from his import CUSTOMER
from mdb import Company, Customer

from bookings.orm import Bookable, Booking


__all__ = ['get_bookable', 'get_bookables', 'get_booking', 'get_bookings']


def get_bookables() -> ModelSelect:
    """Selects bookables."""

    return Bookable.select(Bookable, Customer, Company).join(
        Customer).join(Company).where(Bookable.customer == CUSTOMER.id)


def get_bookable(ident: int) -> Bookable:
    """Returns the respective bookable."""

    return get_bookables().where(Bookable.id == ident).get()


def get_bookings() -> ModelSelect:
    """Selects bookings."""

    return Booking.select(Booking, Bookable, Customer, Company).join(
        Bookable).join(Customer).join(Company).where(
        Bookable.customer == CUSTOMER.id)


def get_booking(ident: int) -> Booking:
    """Returns the respective reservation."""

    return get_bookings().where(Booking.id == ident).get()
