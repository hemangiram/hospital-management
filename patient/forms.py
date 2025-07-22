
from django import forms
from .models import Patient
from .models import MedicalRecord
from .models import Appointment

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')], attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }


       


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'diagnosis', 'prescription', 'doctor_notes', 'visit_date', 'doctors','images']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'prescription': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'doctor_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
        }