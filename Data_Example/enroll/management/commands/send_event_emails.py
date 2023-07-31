from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from enroll.models import Event,EmailTemplate

#from .enroll.models import Event, EmailTemplate


# from  enroll .models import Event, EmailTemplate, EventType, Employee

class Command(BaseCommand):
    help = 'Send automated emails to employees for special events'

    def handle(self, *args, **kwargs):
        current_date = timezone.now().date()
        print(current_date)

        # Step 1: Retrieve event data for the current date

        events = Event.objects.filter(date=current_date, is_sent=False)

        if not events:
            self.stdout.write(self.style.WARNING('No events scheduled for the current date.'))
            return

        for event in events:
            try:
                # Step 2: Retrieve name, event type, and date
                employee_name = event.employee.name
                event_type_name = event.event_type.name

                # Step 3: Fetch the corresponding email template
                email_template = EmailTemplate.objects.get(event_type__name=event_type_name)


                # Step 4: Populate the email template with member's details
                subject = email_template.subject.format(name=employee_name)
                body = email_template.body.format(name=employee_name, event_date=current_date)

                # Step 5: Send the personalized email
                send_mail(subject, body, 'nikitaambulkar.111@gmail.com', [event.employee.email])

                # Update the event as sent and log the sending status
                event.is_sent = True
                event.sent_at = timezone.now()
                event.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully sent email to {event.employee.email}.'))
            except ObjectDoesNotExist as e:
                self.stdout.write(self.style.ERROR(f'Error sending email: {str(e)}'))
            except Exception as e:
                # Log the error and continue with the next event
                event.retries += 1
                event.save()
                self.stdout.write(self.style.ERROR(f'Error sending email: {str(e)}'))
