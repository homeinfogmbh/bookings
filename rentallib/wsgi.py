"""HIS microservice to manage rentables and rents."""

from flask import request

from his import CUSTOMER, Application
from wsgilib import JSON

from rentallib.functions import get_rentable, get_renting
from rentallib.messages import RENTABLE_ADDED
from rentallib.messages import RENTABLE_PATCHED
from rentallib.messages import RENTABLE_DELETED
from rentallib.messages import RENTING_PATCHED
from rentallib.messages import RENTING_DELETED
from rentallib.orm import Rentable, Renting


__all__ = ['APPLICATION']


APPLICATION = Application('renting')


@APPLICATION.route('/rentable', methods=['GET'])
def list_rentables():
    """Lists rentables."""

    return JSON([
        rentable.to_json() for rentable in Rentable.select().where(
            Rentable.customer == CUSTOMER.id)])


@APPLICATION.route('/rentable', methods=['POST'])
def add_rentable():
    """Deletes the respective rentable."""

    rentable = Rentable.from_json(request.json)
    rentable.save()
    return RENTABLE_ADDED.update(id=rentable.id)


@APPLICATION.route('/rentable/<int:ident>', methods=['PATCH'])
def patch_rentable(ident):
    """Deletes the respective rentable."""

    rentable = get_rentable(ident)
    rentable.patch_json(request.json)
    rentable.save()
    return RENTABLE_PATCHED


@APPLICATION.route('/rentable/<int:ident>', methods=['DELETE'])
def delete_rentable(ident):
    """Deletes the respective rentable."""

    get_rentable(ident).delete_instance()
    return RENTABLE_DELETED


@APPLICATION.route('/renting', methods=['GET'])
def list_rentings():
    """Lists available rents."""

    return JSON([
        renting.to_json() for renting in Renting.select().join(Rentable).where(
            Rentable.customer == CUSTOMER.id)])


@APPLICATION.route('/renting/<int:rentable>', methods=['GET'])
def list_rentings_of_rentable(rentable):
    """Returns rentings of the respective rentable."""

    return JSON([
        renting.to_json() for renting in Renting.select().join(Rentable).where(
            (Rentable.customer == CUSTOMER.id)
            & (Renting.rentable == rentable))])


@APPLICATION.route('/renting/<int:ident>', methods=['PATCH'])
def patch_renting(ident):
    """Patches the respective renting."""

    renting = get_renting(ident)
    renting.patch_json(request.json)
    renting.save()
    return RENTING_PATCHED


@APPLICATION.route('/renting/<int:ident>', methods=['DELETE'])
def delete_renting(ident):
    """Deletes the respective renting."""

    get_renting(ident).delete_instance()
    return RENTING_DELETED
