"""Common messages."""

from wsgilib import JSONMessage


__all__ = [
    'NO_SUCH_RENTABLE',
    'RENTABLE_ADDED',
    'RENTABLE_PATCHED',
    'RENTABLE_DELETED',
    'NO_SUCH_RENTING',
    'RENTING_PATCHED',
    'RENTING_DELETED'
]


NO_SUCH_RENTABLE = JSONMessage('No such rentable.', status=404)
RENTABLE_ADDED = JSONMessage('The rentable has been added.', status=201)
RENTABLE_PATCHED = JSONMessage('The rentable has been updated.', status=200)
RENTABLE_DELETED = JSONMessage('The rentable has been deleted.', status=200)
NO_SUCH_RENTING = JSONMessage('No such renting.', status=404)
RENTING_PATCHED = JSONMessage('The renting has been updated.', status=200)
RENTING_DELETED = JSONMessage('The renting has been deleted.', status=200)
