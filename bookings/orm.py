"""Object relational models."""

from datetime import timedelta
from xml.etree.ElementTree import Element, SubElement

from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField

from mdb import Customer
from notificationlib import get_orm_model
from peeweeplus import JSONModel, MySQLDatabase

from rentallib import dom
from rentallib.config import CONFIG
from rentallib.exceptions import AlreadyBooked
from rentallib.exceptions import DurationTooLong
from rentallib.exceptions import DurationTooShort
from rentallib.exceptions import EndBeforeStart


__all__ = ['Bookable', 'Booking']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class _BookingsModel(JSONModel):
    """Base model for rentable stuff."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class Bookable(_BookingsModel):
    """A bookable object."""

    customer = ForeignKeyField(Customer, column_name='customer')
    name = CharField(255)
    type = CharField(255)
    annotation = CharField(255, null=True)
    min_duration = IntegerField(default=30)     # Minimum duration in minutes.
    max_duration = IntegerField(null=True)      # Maximum duration in minutes.

    def book(self, rentee, start, end):
        """Books the rentable."""
        if start > end:
            raise EndBeforeStart()

        if end - start < timedelta(minutes=self.min_duration):
            raise DurationTooShort(self.min_duration)

        if self.max_duration is not None:
            if end - start > timedelta(minutes=self.max_duration):
                raise DurationTooLong(self.max_duration)

        booking = Booking(bookable=self, rentee=rentee, start=start, end=end)
        booking.save()

        try:
            booking.check_conflicts()
        except AlreadyBooked:
            booking.delete_instance()
            raise

        return booking

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


class Booking(_BookingsModel):
    """A booking."""

    bookable = ForeignKeyField(
        Bookable, column_name='bookable', backref='bookings',
        on_delete='CASCADE')
    rentee = CharField(255)
    start = DateTimeField()
    end = DateTimeField()

    def get_conflicts(self):
        """Yields conflicting reservations."""
        cls = type(self)
        cond_not_self = cls.id != self.id
        cond_same_rentable = cls.rentable == self.rentable
        cond_start_within = (cls.start >= self.start) & (cls.start <= self.end)
        cond_end_within = (cls.end > self.start) & (cls.end < self.end)
        cond_overspan = (cls.start < self.end) & (cls.end > self.start)
        cond_conflict = cond_start_within | cond_end_within | cond_overspan
        select = cond_not_self & cond_same_rentable & cond_conflict
        return cls.select().where(select)

    def check_conflicts(self):
        """Checks for conflicting reservations."""
        for reservation in self.get_conflicts():
            raise AlreadyBooked(reservation)

    def to_dom(self):
        """Returns an XML DOM."""
        xml = dom.Booking()
        xml.id = self.id
        xml.bookable = self.bookable.id
        xml.rentee = self.rentee
        xml.start = self.start
        xml.end = self.end
        return xml

    def to_html(self):
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
        header.text = 'Beginn'
        header = SubElement(row, 'th')
        header.text = 'Ende'
        row = SubElement(table, 'tr')
        column = SubElement(row, 'td')
        column.text = self.bookable.name
        column = SubElement(row, 'td')
        column.text = self.rentee
        column = SubElement(row, 'td')
        column.text = self.start.isoformat()    # pylint: disable=E1101
        column = SubElement(row, 'td')
        column.text = self.end.isoformat()  # pylint: disable=E1101
        return html

    def to_text(self):
        """Returns a text message."""
        text = 'Sehr geehrte Damen und Herren,\n\n'
        text += 'die folgende Reservierung wurde eingetragen:\n\n'
        text += f'{self.bookable.name} durch {self.rentee}'
        start = self.start.isoformat()  # pylint: disable=E1101
        end = self.end.isoformat()  # pylint: disable=E1101
        text += f' von {start} bis {end}.'
        return text


NotificationEmail = get_orm_model(_BookingsModel)
