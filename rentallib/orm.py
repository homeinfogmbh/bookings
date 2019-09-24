"""Object relational models."""

from datetime import timedelta

from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField

from mdb import Customer
from peeweeplus import JSONModel, MySQLDatabase

from rentallib import dom
from rentallib.config import CONFIG
from rentallib.exceptions import AlreadyRented
from rentallib.exceptions import DurationTooLong
from rentallib.exceptions import DurationTooShort
from rentallib.exceptions import EndBeforeStart


__all__ = ['Rentable', 'Renting']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class BaseModel(JSONModel):
    """Base model for rentable stuff."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class Rentable(BaseModel):
    """A rentable object."""

    customer = ForeignKeyField(Customer, column_name='customer')
    name = CharField(255)
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

    def to_dom(self):
        """Returns an XML DOM."""
        xml = dom.Rentable()
        xml.id = self.id
        xml.customer = self.customer.id
        xml.name = self.name
        xml.type = self.type
        xml.annotation = self.annotation
        xml.min_duration = self.min_duration
        xml.max_duration = self.max_duration
        return xml


class Renting(BaseModel):
    """Reservation of a rentable."""

    rentable = ForeignKeyField(
        Rentable, column_name='rentable', backref='rentings',
        on_delete='CASCADE')
    rentee = CharField(255)
    start = DateTimeField()
    end = DateTimeField()

    def get_conflicts(self):
        """Yields conflicting rentings."""
        cls = type(self)
        cond_not_self = cls.id != self.id
        cond_same_rentable = cls.rentable == self.rentable
        cond_start_within = (cls.start >= self.start) & (cls.start <= self.end)
        cond_end_within = (cls.end > self.start) & (cls.end <= self.end)
        cond_overspan = (cls.start < self.end) & (cls.end > self.start)
        cond_conflict = cond_start_within | cond_end_within | cond_overspan
        select = cond_not_self & cond_same_rentable & cond_conflict
        return cls.select().where(select)

    def check_conflicts(self):
        """Checks for conflicting rentings."""
        for renting in self.get_conflicts():
            raise AlreadyRented(renting)

    def to_dom(self):
        """Returns an XML DOM."""
        xml = dom.Renting()
        xml.id = self.id
        xml.rentable = self.rentable.id
        xml.rentee = self.rentee
        xml.start = self.start
        xml.end = self.end
        return xml
