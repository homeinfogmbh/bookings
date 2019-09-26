"""Emailing of new bookings."""

from xml.etree.ElementTree import tostring

from emaillib import EMail
from functoolsplus import coerce
from notificationlib import get_email_func

from bookings.config import CONFIG
from bookings.orm import NotificationEmail


__all__ = ['email']


@coerce(frozenset)
def get_emails(booking):
    """Yields notification emails."""

    for notification_email in NotificationEmail.select().where(
            NotificationEmail.customer == booking.bookable.customer):
        recipient = notification_email.email
        subject = notification_email.subject or CONFIG['email']['subject']
        sender = CONFIG['email']['from']

        if notification_email.html:
            html = tostring(
                booking.to_html(), encoding='unicode', method='html')
        else:
            html = None

        plain = None if notification_email.html else booking.to_text()
        yield EMail(subject, sender, recipient, plain=plain, html=html)


email = get_email_func(get_emails)  # pylint: disable=C0103