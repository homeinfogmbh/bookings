"""HIS microservice to manage rentables and rents."""

from flask import request

from his import admin, authenticated, authorized, CUSTOMER, Application
from notificationlib import get_wsgi_funcs
from wsgilib import JSON

from rentallib.functions import get_rentable, get_renting
from rentallib.messages import RENTABLE_ADDED
from rentallib.messages import RENTABLE_PATCHED
from rentallib.messages import RENTABLE_DELETED
from rentallib.messages import RENTING_PATCHED
from rentallib.messages import RENTING_DELETED
from rentallib.orm import Rentable, Renting, NotificationEmail


__all__ = ['APPLICATION']


APPLICATION = Application('renting')


@authenticated
@authorized('renting')
def list_rentables():
    """Lists rentables."""

    return JSON([
        rentable.to_json() for rentable in Rentable.select().where(
            Rentable.customer == CUSTOMER.id)])


@authenticated
@admin
@authorized('renting')
def add_rentable():
    """Deletes the respective rentable."""

    rentable = Rentable.from_json(request.json)
    rentable.save()
    return RENTABLE_ADDED.update(id=rentable.id)


@authenticated
@admin
@authorized('renting')
def patch_rentable(ident):
    """Deletes the respective rentable."""

    rentable = get_rentable(ident)
    rentable.patch_json(request.json)
    rentable.save()
    return RENTABLE_PATCHED


@authenticated
@admin
@authorized('renting')
def delete_rentable(ident):
    """Deletes the respective rentable."""

    get_rentable(ident).delete_instance()
    return RENTABLE_DELETED


@authenticated
@authorized('renting')
def list_rentings():
    """Lists available rents."""

    return JSON([
        renting.to_json() for renting in Renting.select().join(Rentable).where(
            Rentable.customer == CUSTOMER.id)])


@authenticated
@authorized('renting')
def list_rentings_of_rentable(rentable):
    """Returns rentings of the respective rentable."""

    return JSON([
        renting.to_json() for renting in Renting.select().join(Rentable).where(
            (Rentable.customer == CUSTOMER.id)
            & (Renting.rentable == rentable))])


@authenticated
@authorized('renting')
def patch_renting(ident):
    """Patches the respective renting."""

    renting = get_renting(ident)
    renting.patch_json(request.json)
    renting.save()
    return RENTING_PATCHED


@authenticated
@authorized('renting')
def delete_renting(ident):
    """Deletes the respective renting."""

    get_renting(ident).delete_instance()
    return RENTING_DELETED


GET_EMAILS, SET_EMAILS = get_wsgi_funcs('renting', NotificationEmail)


APPLICATION.add_routes((
    ('GET', '/rentable', list_rentables),
    ('POST', '/rentable', add_rentable),
    ('PATCH', '/rentable/<int:ident>', patch_rentable),
    ('DELETE', '/rentable/<int:ident>', delete_rentable),
    ('GET', '/renting', list_rentings),
    ('GET', '/renting/<int:rentable>', list_rentings_of_rentable),
    ('PATCH', '/renting/<int:ident>', patch_renting),
    ('DELETE', '/renting/<int:ident>', delete_renting),
    ('GET', '/email', GET_EMAILS, 'get_emails'),
    ('POST', '/email', SET_EMAILS, 'set_emails')
))
