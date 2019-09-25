"""Common functions."""

from his import CUSTOMER

from rentallib.messages import NO_SUCH_RENTABLE, NO_SUCH_RENTING
from rentallib.orm import Rentable, Renting


__all__ = ['get_rentable', 'get_renting']


def get_rentable(ident):
    """Returns the respective rentable."""

    try:
        return Rentable.get(
            (Rentable.id == ident) & (Rentable.customer == CUSTOMER.id))
    except Rentable.DoesNotExist:
        raise NO_SUCH_RENTABLE


def get_renting(ident):
    """Returns the respective renting."""

    try:
        return Renting.select().join(Rentable).where(
            (Renting.id == ident) & (Rentable.customer == CUSTOMER.id)
        ).get()
    except Renting.DoesNotExist:
        raise NO_SUCH_RENTING
