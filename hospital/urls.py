"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', home,name='home'),
    path('login/', login, name='login'),
    path('patient', add,name='add_patient'),
    path('medical', add_record, name='medical'),
    path('appoiment',book_appointment, name='appoiment'),
    path('doctor', doctor,name='doctor'),
    path('nurse', nurse,name='nurse'),
    path('reception', reception,name='reception'),
    path('ward', ward_status, name='ward_status'),
    path('bill', billing_view,name='billing'),
    path('logout', logout_view, name='logout'),
    path('role', role_view, name='role'),
    path('record/<int:record_id>/', record_detail, name='record_detail'),
    path('patient/<int:patient_id>/', detail_patient, name='detail_patient'),
    path('show_patient/', show_patient, name='show_patient'),
    path('show_record/', show_record, name='show_record'),
    path('patients/<int:pk>/edit/', edit_patient, name='edit_patient'),
    path('patients/<int:pk>/delete/', delete_patient, name='delete_patient'),
    path('patients/<int:pk>/', view_patient, name='view_patient'),
    path('records/<int:pk>/', view_medical_record, name='view_record'), 
    path('records/<int:pk>/edit/', edit_medical_record, name='edit_record'), 
    path('records/<int:pk>/delete/', delete_medical_record, name='delete_record'),  
   





]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)