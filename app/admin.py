from django.contrib import admin
from .models import User_Details, Patient,FieldTypes, Doctor, Appointment
# Register your models here.

admin.site.register(User_Details)
admin.site.register(Patient)
admin.site.register(FieldTypes)
admin.site.register(Doctor)
admin.site.register(Appointment)