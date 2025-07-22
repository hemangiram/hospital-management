from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


ROLE_CHOICES = [
    ('doctor', 'Doctor'),
    ('nurse', 'Nurse'),
    ('admin', 'Admin'),
    ('user', 'User'),
    ('receptionist', 'Receptionist'),
]




class Doctor(models.Model):
        name = models.CharField(max_length=100)
        department = models.CharField(max_length=100)
        specialization = models.CharField(max_length=100)
        image = models.ImageField(upload_to='doctors/', null=True, blank=True) 
        desc = models.TextField(max_length=100)


        def __str__(self):
           return self.name
    
class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    doctors = models.ManyToManyField(Doctor, related_name='patients')
    def __str__(self):
        return self.name



class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    prescription = models.TextField()
    doctor_notes = models.TextField(blank=True, null=True)
    visit_date = models.DateField(default=timezone.now)
    doctors = models.ManyToManyField(Doctor, related_name='medical_records')
    images = models.ImageField(upload_to='medical_records/', null=True, blank=True)
    # def __str__(self):
    #     return f"{self.patient.name} - {self.visit_date}"
    


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.date}"
    




class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)
    modules = models.ManyToManyField('Module', related_name='modules')
    can_edit = models.BooleanField(default=False)
    can_delete_patient = models.BooleanField(default=False)
    can_view_patient = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    

    
class Update(models.Model):
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    view_report = models.BooleanField(default=True)
    delete_report = models.BooleanField(default=False)
    edit_report = models.BooleanField(default=False)

   
    
class Module(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    last_session_key = models.CharField(max_length=40, blank=True, null=True)
    @property
    def role_name(self):
      return self.role.name.lower()

class Ward(models.Model):
    number = models.IntegerField()
    ward_type = models.CharField(max_length=100)  # e.g. ICU, General, Maternity
    capacity = models.IntegerField()
    occupied = models.IntegerField()

    def __str__(self):
        return f"Ward {self.number} - {self.ward_type}"



class Billing(models.Model):
    patient_name = models.CharField(max_length=100)
    service = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receptionist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill for {self.patient_name} - ₹{self.amount}"
    
  