from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
import geocoder


class User_Details(models.Model):
	username = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
	aadhaar = models.IntegerField(blank=True)
	f_name = models.CharField(max_length=25, blank=True)
	l_name = models.CharField(max_length=25, blank=True)
	address = models.TextField(max_length=100, blank=True)
	phone_no = models.IntegerField(blank=True)
	gender = models.CharField(max_length=1)
	is_doctor = models.BooleanField(default = False)
	is_patient = models.BooleanField(default = False)
	g = geocoder.ip('me')
	lat = models.FloatField(default=g.latlng[0])
	lng = models.FloatField(default=g.latlng[1])

	def __str__(self):
		return self.username.username

class Patient(models.Model):
	patient = models.OneToOneField(User_Details, on_delete=models.CASCADE, primary_key=True)

	def __str__(self):
		return self.patient.username.username

class FieldTypes(models.Model):
	field = models.CharField(max_length=25)

	def __str__(self):
		return self.field

class Doctor(models.Model):
	doctor = models.OneToOneField(User_Details, on_delete=models.CASCADE, primary_key=True)
	field = models.ForeignKey(FieldTypes, on_delete=models.CASCADE)
	def __str__(self):
		return (self.doctor.username.username+" - "+ self.field.field)

class Appointment(models.Model):
	a_id = models.AutoField(primary_key=True)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	date = models.CharField(max_length=10)
	schedule = models.CharField(max_length=500)

	def __str__(self):
		return (self.doctor.doctor.username.username+"-"+self.patient.patient.username.username+"-"+self.date)