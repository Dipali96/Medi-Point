"""medipoint1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homapage,name='homapage'),
    path('pregister/',views.pregister,name="pregister"),
    path('dregister/',views.dregister,name="dregister"),
    path('login/',views.ulogin, name="login"),
    path('logout/',views.ulogout, name="logout"),
    path('pprofile/',views.pprofile,name="pprofile"),
    path('dprofile/',views.dprofile,name="dprofile"),
    #path('doctor-bookings/',views.dbookings,name="dbookings"),
    path('schedule-booking/',views.sbookings,name="sbookings"),
    path('patient-bookings/',views.pbookings,name="pbookings"),
    path('doctor/<str:name>/',views.doctor,name="doctor"),
]

if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)