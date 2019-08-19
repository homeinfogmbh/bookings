"""Object relational models."""

from datetime import datetime, timedelta

from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import Model

from mdb import Customer
from peeweeplus import MySQLDatabase

from rentallib.config import CONFIG
from rentallib.exceptions import AlreadyRented
from rentallib.exceptions import DurationTooLong
from rentallib.exceptions import DurationTooShort
from rentallib.exceptions import EndBeforeStart


__all__ = ['Rentable', 'Renting']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class BaseModel(Model):
    """Base model for rentable stuff."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class Rentable(BaseModel):
    """A rentable object."""

    customer = ForeignKeyField(Customer, column_name='customer')
    identifier = CharField(255)
    type = CharField(255)
    annotation = CharField(255, null=True)
    min_duration = IntegerField(default=30)     # Minimum duration in minutes.
    max_duration = IntegerField(null=True)      # Maximum duration in minutes.

    def rent(self, rentee, start, end):
        """Rents the rentable."""
        if start > end:
            raise EndBeforeStart()

        if end - start < timedelta(minutes=self.min_duration):
            raise DurationTooShort(self.min_duration)

        if self.max_duration is not None:
            if end - start > timedelta(minutes=self.max_duration):
                raise DurationTooLong(self.max_duration)

        renting = Renting(rentable=self, rentee=rentee, start=start, end=end)
        renting.save()

        try:
            renting.check_conflicts()
        except AlreadyRented:
            renting.delete_instance()
            raise

        return renting


class Renting(BaseModel):
    """Reservation of a rentable."""

    rentable = ForeignKeyField(
        Rentable, column_name='rentable', backref='rentings',
        on_delete='CASCADE')
    rentee = CharField(255)
    rented = DateTimeField(default=datetime.now)
    start = DateTimeField()
    end = DateTimeField()

    @classmethod
    def timespans(cls, rentable):
        """Yields renting time spans."""
        for renting in cls.select().where(cls.rentable == rentable):
            yield (renting.start, renting.end)

    def check_conflicts(self):
        """Checks for conflicting rentings."""
        cls = type(self)

        for renting in cls.select().where(
                (cls.rentable == self.rentable) & (cls.id != self.id)):
            if self.start < renting.start < self.end:
                raise AlreadyRented(renting)

            if self.start < renting.end < self.end:
                raise AlreadyRented(renting)

            if self.start <= renting.start and self.end >= renting.end:
                raise AlreadyRented(renting)
