"""Object relational models."""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Iterable
from xml.etree.ElementTree import Element, SubElement

from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import ModelSelect

from mdb import Company, Customer
from notificationlib import get_email_orm_model
from peeweeplus import JSONModel, MySQLDatabaseProxy

from bookings import dom
from bookings.exceptions import AlreadyBooked
from bookings.exceptions import DurationTooLong
from bookings.exceptions import DurationTooShort
from bookings.exceptions import EndBeforeStart


__all__ = ['Bookable', 'Booking']


DATABASE = MySQLDatabaseProxy('bookings')


class _BookingsModel(JSONModel):
    """Base model for bookings database."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class Bookable(_BookingsModel):
    """A bookable object."""

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE', lazy_load=False)
    name = CharField(255)
    type = CharField(255)
    annotation = CharField(255, null=True)
    min_duration = IntegerField(default=30)     # Minimum duration in minutes.
    max_duration = IntegerField(null=True)      # Maximum duration in minutes.

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects records."""
        if not cascade:
            return super().select(*args, **kwargs)

        return cls.select(cls, Customer, Company).join(Customer).join(Company)

    def book(self, start: datetime, end: datetime, *,
             rentee: str = None, purpose: str = None) -> Booking:
        """Books the rentable."""
        if start > end:
            raise EndBeforeStart()

        if end - start < timedelta(minutes=self.min_duration):
            raise DurationTooShort(self.min_duration)

        if self.max_duration is not None:
            if end - start > timedelta(minutes=self.max_duration):
                raise DurationTooLong(self.max_duration)

        booking = Booking(
            bookable=self, rentee=rentee, purpose=purpose, start=start,
            end=end)
        booking.save()

        try:
            booking.check_conflicts()
        except AlreadyBooked:
            booking.delete_instance()
            raise

        return booking

    def to_dom(self) -> dom.Bookable:
        """Returns an XML DOM."""
        xml = dom.Bookable()
        xml.id = self.id
        xml.customer = self.customer.id
        xml.name = self.name
        xml.type = self.type
        xml.annotation = self.annotation
        xml.min_duration = self.min_duration
        xml.max_duration = self.max_duration
        return xml


class Booking(_BookingsModel):
    """A booking."""

    bookable = ForeignKeyField(
        Bookable, column_name='bookable', backref='bookings',
        on_delete='CASCADE', lazy_load=False)
    rentee = CharField(255, null=True)
    purpose = CharField(255, null=True)
    start = DateTimeField()
    end = DateTimeField()

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects records."""
        if not cascade:
            return super().select(*args, **kwargs)

        return cls.select(cls, Bookable, Customer, Company).join(
            Bookable).join(Customer).join(Company)

    def get_conflicts(self) -> Iterable[Booking]:
        """Yields conflicting bookings."""
        cls = type(self)
        cond_not_self = cls.id != self.id
        cond_same_bookable = cls.bookable == self.bookable
        cond_overlap = (cls.start < self.end) & (cls.end > self.start)
        conditions = cond_not_self & cond_same_bookable & cond_overlap
        return cls.select().where(conditions)

    def check_conflicts(self):
        """Checks for conflicting bookings."""
        conflicts = tuple(self.get_conflicts())

        if conflicts:
            raise AlreadyBooked(conflicts)

    def to_dom(self) -> dom.Booking:
        """Returns an XML DOM."""
        xml = dom.Booking()
        xml.id = self.id
        xml.bookable = self.bookable.id
        xml.rentee = self.rentee
        xml.purpose = self.purpose
        xml.start = self.start
        xml.end = self.end
        return xml

    def to_html(self) -> Element:
        """Returns a HTML message."""
        html = Element('html')
        header = SubElement(html, 'header')
        SubElement(header, 'meta', attrib={'charset': 'UTF-8'})
        title = SubElement(header, 'title')
        title.text = 'Neue Buchung'
        body = SubElement(html, 'body')
        salutation = SubElement(body, 'span')
        salutation.text = 'Sehr geehrte Damen und Herren,'
        SubElement(body, 'br')
        SubElement(body, 'br')
        text = SubElement(body, 'span')
        text.text = 'die folgende Reservierung wurde eingetragen:'
        SubElement(body, 'br')
        SubElement(body, 'br')
        table = SubElement(body, 'table', attrib={'border': '1'})
        row = SubElement(table, 'tr')
        header = SubElement(row, 'th')
        header.text = 'Gemietetes Objekt'
        header = SubElement(row, 'th')
        header.text = 'Mieter'
        header = SubElement(row, 'th')
        header.text = 'Verwendungszweck'
        header = SubElement(row, 'th')
        header.text = 'Beginn'
        header = SubElement(row, 'th')
        header.text = 'Ende'
        row = SubElement(table, 'tr')
        column = SubElement(row, 'td')
        column.text = self.bookable.name
        column = SubElement(row, 'td')
        column.text = self.rentee or '–'
        column = SubElement(row, 'td')
        column.text = self.purpose or '–'
        column = SubElement(row, 'td')
        column.text = self.start.isoformat()    # pylint: disable=E1101
        column = SubElement(row, 'td')
        column.text = self.end.isoformat()  # pylint: disable=E1101
        return html

    def to_text(self) -> str:
        """Returns a text message."""
        text = 'Sehr geehrte Damen und Herren,\n\n'
        text += 'die folgende Reservierung wurde eingetragen:\n\n'
        text += f'{self.bookable.name}\n'

        if self.rentee is not None:
            text += f' durch {self.rentee}\n'

        if self.purpose is not None:
            text += f' zwecks {self.purpose}\n'

        start = self.start.isoformat()  # pylint: disable=E1101
        end = self.end.isoformat()  # pylint: disable=E1101
        text += f' von {start} bis {end}.'
        return text


NotificationEmail = get_email_orm_model(_BookingsModel)
