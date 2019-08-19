"""HIS microservice to manage rentables and rents."""

from flask import request

from his import CUSTOMER, Application
from wsgilib import JSON, JSONMessage

from rentallib.orm import Rentable


__all__ = ['APPLICATION']


APPLICATION = Application('renting')
NO_SUCH_RENTABLE = JSONMessage('No such rentable.', status=404)
RENTABLE_ADDED = JSONMessage('The rentable has been added.', status=201)
RENTABLE_PATCHED = JSONMessage('The rentable has been updated.', status=200)
RENTABLE_DELETED = JSONMessage('The rentable has been deleted.', status=200)


def get_rentable(ident):
    """Returns the respective rentable."""

    try:
        return Rentable.get(
            (Rentable.id == ident) & (Rentable.customer == CUSTOMER.id))
    except Rentable.DoesNotExist:
        raise NO_SUCH_RENTABLE


@APPLICATION.route('/rentables', methods=['GET'])
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
