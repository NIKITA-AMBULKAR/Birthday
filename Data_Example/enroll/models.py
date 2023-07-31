from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class EventType(models.Model):
    name = models.CharField(max_length=50)

class Event(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    date = models.DateField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    retries = models.PositiveIntegerField(default=0)



class EmailTemplate(models.Model):
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    body = models.TextField()
