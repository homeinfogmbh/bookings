"""Emailing of new bookings."""

from typing import Iterator
from xml.etree.ElementTree import tostring

from emaillib import EMail
from functoolsplus import coerce
from notificationlib import get_email_func

from bookings.config import get_config
from bookings.orm import Booking, NotificationEmail


__all__ = ['email']


@coerce(frozenset)
def get_emails(booking: Booking) -> Iterator[EMail]:
    """Yields notification emails."""

    for notification_email in NotificationEmail.select().where(
            NotificationEmail.customer == booking.bookable.customer):
        recipient = notification_email.email
        sender = (config := get_config()).get('email', 'from')
        subject = notification_email.subject or config.get('email', 'subject')

        if notification_email.html:
            html = tostring(
                booking.to_html(), encoding='unicode', method='html')
        else:
            html = None

        plain = None if notification_email.html else booking.to_text()
        yield EMail(subject, sender, recipient, plain=plain, html=html)


email = get_email_func(get_emails)  # pylint: disable=C0103
