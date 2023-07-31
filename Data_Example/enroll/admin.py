# admin.py
from django.contrib import admin
from .models import Employee, Event,EventType,EmailTemplate

admin.site.register(Employee)
admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(EmailTemplate)


