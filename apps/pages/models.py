from django.db import models
from django.urls import reverse
from apps.accounts.models import CustomAccount
from enum import Enum
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Class representing Trip Status, subclass of Enum
class TripStatusList_(Enum):
    YTS = "Yet to start"
    IP = "In progress"
    CP = "Completed"
    AR = "Awaiting response"


class Trip(models.Model):
    trip_owner = models.ForeignKey(
        CustomAccount,
        on_delete=models.CASCADE,
        related_name='trips'
    )
    trip_location = models.CharField(max_length=30)
    trip_name = models.CharField(max_length=30)
    trip_start = models.DateTimeField()
    trip_end = models.DateTimeField()
    trip_status = models.CharField(
        max_length=30,
        choices=[(tag, tag.value) for tag in TripStatusList_]
    )
    response_sent = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)

    def update_status(self):
        """
        Update the status of the trip object in the database.
        """
        # Get trip date information
        start = self.trip_start
        end = self.trip_end
        now = timezone.now()

        # Upcoming
        if now < start <= now + timedelta(days=7):
            self.trip_status = TripStatusList_.YTS.value

        # In progress
        if start <= now < end:
            self.trip_status = TripStatusList_.IP.value

        # Awaiting Response
        if end < now < end + timedelta(hours=1):
            self.trip_status = TripStatusList_.AR.value

        # Complete
        if end < now - timedelta(hours=1):
            self.trip_status = TripStatusList_.CP.value

        # Save changes in the database
        self.save()

    def send_notification_email(self):
        """
        Send an email to the trip owner when a trip is 'Awaiting response'.
        """
        # Define email fields
        sender = 'staysafe3308@gmail.com'
        subject = f'Awaiting response for trip to: {self.trip_location}!'
        emergency_contact_date = (self.trip_end + timedelta(hours=1)).strftime(
            '%l:%m%p on %b %d, %Y'
        )
        # Send an email notifying the user that a trip is awaiting response
        HTML_message = render_to_string(
            'notification_email.html',
            {
                'first_name': self.trip_owner.first_name,
                'last_name': self.trip_owner.last_name,
                'trip_location': self.trip_location,
                'contact_date': emergency_contact_date,
            }
        )
        message = strip_tags(HTML_message)
        send_mail(subject, message, sender, [self.trip_owner.email],
                  html_message=HTML_message)

    def send_contact_emails(self):
        """
        Send an email to all of the trip owner's emergency contacts.
        """
        # Define email fields
        name_list = [
            c.first_name for c in EmergencyContact.objects.filter(
                user=self.trip_owner
            )
        ]
        email_list = [
            c.email for c in EmergencyContact.objects.filter(
                user=self.trip_owner
            )
        ]
        end_date = self.trip_end.strftime('%l:%m%p on %b %d, %Y')
        sender = 'staysafe3308@gmail.com'
        subject = f'{self.trip_owner.first_name} {self.trip_owner.last_name}'\
                  f'\'s trip ended!'

        # Send an email to each emergency contact
        for contact_name, contact_email in zip(name_list, email_list):
            HTML_message = render_to_string(
                'contact_email.html',
                {
                    'contact': contact_name,
                    'first_name': self.trip_owner.first_name,
                    'last_name': self.trip_owner.last_name,
                    'trip_location': self.trip_location,
                    'end_date': end_date,
                    'email': self.trip_owner.email,
                }
            )
            message = strip_tags(HTML_message)
            send_mail(subject, message, sender, [contact_email],
                      html_message=HTML_message)

    def __str__(self):
        return self.trip_name

    def get_absolute_url(self):
        return reverse('home', args=[str(self.id)])


class EmergencyContact(models.Model):
    user = models.ForeignKey(
        CustomAccount,
        on_delete=models.CASCADE,
        related_name='emergency_contacts'
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(
        blank=True,
        max_length=30,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
