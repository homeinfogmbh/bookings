"""HIS microservice to manage rentables and rents."""

from flask import request

from his import CUSTOMER, Application
from wsgilib import JSON, JSONMessage

from rentallib.orm import Rentable, Renting


__all__ = ['APPLICATION']


APPLICATION = Application('renting')
NO_SUCH_RENTABLE = JSONMessage('No such rentable.', status=404)
RENTABLE_ADDED = JSONMessage('The rentable has been added.', status=201)
RENTABLE_PATCHED = JSONMessage('The rentable has been updated.', status=200)
RENTABLE_DELETED = JSONMessage('The rentable has been deleted.', status=200)
NO_SUCH_RENTING = JSONMessage('No such renting.', status=404)
RENTING_PATCHED = JSONMessage('The renting has been updated.', status=200)
RENTING_DELETED = JSONMessage('The renting has been deleted.', status=200)


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
        return Renting.get(
            (Renting.id == ident) & (Renting.customer == CUSTOMER.id))
    except Renting.DoesNotExist:
        raise NO_SUCH_RENTING


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
