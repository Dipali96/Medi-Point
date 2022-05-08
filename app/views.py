from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import geocoder
from math import sin, cos, sqrt, atan2, radians
from .models import User_Details, Patient,FieldTypes, Doctor, Appointment

# Create your views here.
def loc(a,b,lat,lag):
	R = 6373.0
	lat1 = radians(a)
	lon1 = radians(b)
	lat2 = radians(lat)
	lon2 = radians(lag)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	print(distance)
	return distance

def homapage(request):
	return render(request, "index.html")

def pregister(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		try:
			user = User.objects.create_user(username=username, password=password)
			profile = User_Details()
			profile.username = user
			profile.is_patient = True
			profile.aadhaar = request.POST['aadhaar']
			profile.f_name = request.POST['f_name']
			profile.l_name = request.POST['l_name']
			profile.address = request.POST['address']
			profile.gender = request.POST['gender']
			profile.phone_no = request.POST['phone_no']
			profile.save()
			pat = Patient()
			pat.patient = profile
			pat.save()
			return redirect("login")
		except Exception as ex:
			print(ex)
			return render(request, "pregister.html",{'error_message':'Username already exists'})
	else:
		return render(request, "pregister.html")

def dregister(request):
	f = FieldTypes.objects.all()
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		try:
			user = User.objects.create_user(username=username, password=password)
			profile = User_Details()
			profile.username = user
			profile.is_doctor = True
			profile.aadhaar = request.POST['aadhaar']
			profile.f_name = request.POST['f_name']
			profile.l_name = request.POST['l_name']
			profile.address = request.POST['address']
			profile.gender = request.POST['gender']
			profile.phone_no = request.POST['phone_no']
			profile.save()
			doc = Doctor()
			doc.Doctor = profile
			field = request.POST['field']
			fi = FieldTypes.objects.get(field=field)
			doc.field = fi
			doc.save()
			return redirect("login")
		except Exception as ex:
			print(ex)
			return render(request, "dregister.html",{'error_message':'Username already exists', "f":f})
	else:
		return render(request, "dregister.html", {"f":f})

def ulogin(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		user     = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				details = User_Details.objects.get(username=user)
				if details.is_patient:
					return redirect("pprofile")
				else:
					return redirect("dprofile")
			else:
				return render(request,'login.html',{'error_message':'Your account is disabled'})
		else:
			return render(request,'login.html',{'error_message': 'Invalid Login'})
	else:
		return render(request, "login.html")

@login_required
def ulogout(request):
	logout(request)
	return redirect('homapage')

@login_required
def pprofile(request):
	user = request.user
	print(user)
	user_profile = User_Details.objects.get(username=user)
	if request.method=="POST":
		user_profile.aadhaar = request.POST['aadhaar']
		user_profile.f_name = request.POST['f_name']
		user_profile.l_name = request.POST['l_name']
		user_profile.address = request.POST['address']
		user_profile.gender = request.POST['gender']
		user_profile.phone_no = request.POST['phone_no']
		user_profile.save()

	return render(request, "pprofile.html",{"profile": user_profile})

@login_required
def dprofile(request):
	user = request.user
	print(user)
	user_profile = User_Details.objects.get(username=user)
	doc = Doctor.objects.get(doctor=user_profile)
	if request.method=="POST":
		user_profile.aadhaar = request.POST['aadhaar']
		user_profile.f_name = request.POST['f_name']
		user_profile.l_name = request.POST['l_name']
		user_profile.address = request.POST['address']
		user_profile.gender = request.POST['gender']
		user_profile.phone_no = request.POST['phone_no']
		user_profile.save()

	return render(request, "dprofile.html",{"profile": user_profile, "doc":doc})

@login_required
def pbookings(request):
	current_user = request.user
	ud = User_Details.objects.get(username=current_user)
	doc = Doctor.objects.get(doctor=ud)
	appo = Appointment.objects.filter(doctor=doc)
	return HttpResponse(appo)


@login_required
def sbookings(request):
	fields = FieldTypes.objects.all()
	g = geocoder.ip('me')
	lat = g.latlng[0]
	lag = g.latlng[1]
	r = []
	if request.method=="POST":
		field = FieldTypes.objects.get(field=request.POST["field"])
		docs = Doctor.objects.filter(field=field)
		for i in docs:
			a = i.lat
			b = i.lng
			if loc(a,b,lat,lag)<1.5:
				r.append(i)
		return render(request, "sbookings.html", {"field":field,"docs":r, "a":True})
	return render(request, "sbookings.html",{"fields":fields, "a":False})

@login_required
def doctor(request,name):
	user1 = User.objects.get(username=name)
	profile = User_Details.objects.get(username=user1)
	doc = Doctor.objects.get(doctor=profile)
	appointment = Appointment.objects.filter(doctor=doc).first()
	if not appointment:
		return HttpResponse("No appointments booked")
	return HttpResponse(appointment.schedule)
	pass


# s = "{"04/10/22":{"13:00-14:00":"keshav"}}"
# d = eval(s)
# f = str(d)