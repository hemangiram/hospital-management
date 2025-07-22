from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from patient.forms import PatientForm
from patient.forms import MedicalRecordForm,AppointmentForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from patient.models import Ward
from django.contrib.auth import logout
from patient.models import Billing
from django.contrib.auth.decorators import login_required
from patient.decorator import allow_roles
from urllib.parse import urlparse
from dynamic.models import Service,Department
from patient.models import UserProfile
from patient.models import MedicalRecord
from patient.models import Patient, Doctor ,Role, Module    
from django.shortcuts import render, get_object_or_404, redirect
from patient.models import Patient,Update
from patient.forms import PatientForm 


def home(request):
    services = Service.objects.all()
    departments = Department.objects.all()
    user_Profile = request.user.userprofile
    role = request.user.userprofile.role.name.lower()
    if role == 'admin':
        modules = Module.objects.all()  # Show all modules
    else:
        modules = user_Profile.role.modules.all()
    print("request:", request.user.userprofile.role.modules)
    print(f"User role: {modules}")
    print(f"User role: {role}")

    return render(request, "index.html", {
        'services': services,
        'departments': departments,
        'role': role,
        'modules': modules 
    })



def add(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detail_patient', patient_id=form.instance.id)   # Redirect after saving
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})


def add_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save()  # Save and get object
            return redirect('record_detail', record_id=record.id) 
    else:
        form = MedicalRecordForm()
    return render(request, 'medical.html', {'form': form})




def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'index.html')
    else:
        form = AppointmentForm()
    return render(request, 'index.html', {'form': form})






def login(request):
  from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from urllib.parse import urlparse

def login(request):
    if request.method == 'POST':
 
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or request.GET.get('next')

        
        user = authenticate(request, username=username, password=password)

        if user:
            print(f"User authenticated: {user.username}")

           
            auth_login(request, user)
            profile, created = UserProfile.objects.get_or_create(user=user)

            print(f"User profile role: {profile.role.name if profile.role else 'No role assigned'}")

            if user.is_superuser:
                return redirect('/admin/')

            role = profile.role.name.lower() if profile.role else None

        
            if next_url:
                path = urlparse(next_url).path
                print(f"Redirecting to next URL: {path}")

                allowed_paths = {
                    'doctor': ['/doctor'],
                    'nurse': ['/nurse', '/doctor'],
                    'receptionist': ['/reception'],
                }

                if path in allowed_paths.get(role, []):
                    return redirect(path)

            if role == 'doctor':
                return redirect('doctor')  
            elif role == 'nurse':
                return redirect('nurse') 
            elif role == 'receptionist':
                return redirect('reception')  
            else:
                return redirect('home')  

        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')



def ward_status(request):
    wards = Ward.objects.all()
    return render(request, 'ward_status.html', {'wards': wards})


@allow_roles(['doctor'])
def doctor(request):
       return render(request,"doctor.html",{'hide_menu': True})

@allow_roles(['nurse','doctor'])
def nurse(request):
    return render(request,"nurse.html",{'nurse_menu':True})
@allow_roles(['receptionist'])
def reception(request):
    role = request.user.userprofile.role.name.lower()
    modules =request.user.userprofile.role.modules.all()
  
    context = {
         'role':role,
         'modules': modules,

    }

    return render(request,"reception.html",context)

  


@login_required
def billing_view(request):
     user = request.user
     role = getattr(user.userprofile, 'role', 'unknown') 

     if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        service = request.POST.get('service')
        amount = request.POST.get('amount')

       
        Billing.objects.create(
            patient_name=patient_name,
            service=service,
            amount=amount,
            receptionist=user 
        )

        messages.success(request, "Billing record saved successfully.")
        return redirect('billing')
 
     return render(request, 'billing.html', {'user': user, 'role': role})


def logout_view(request):
    print("heloo")
    logout(request)
    return redirect('login') 





def dashboard_view(request):
    can_see_medical = request.user.groups.filter(name__in=["doctor", "nurse"]).exists()
    return render(request, 'medical.html', {
        'can_see_medical': can_see_medical
    })

def role_view(request):
    if not request.user.is_authenticated:
        print("User not authenticated, redirecting to login")
        return redirect('login')

    user_profile = getattr(request.user, 'userprofile', None)
    role = getattr(user_profile, 'role', None)

    if not role:
        return render(request, 'role.html', {
            'role': 'No role assigned',
            'modules': []
        })

    modules = role.modules.all() 
    print("Role:", role.name)
    print("Modules:", ', '.join(module.name for module in modules))

    return render(request, 'role.html', {
        'role': role.name,
        'modules': modules
    })




def record_detail(request, record_id):
    record = MedicalRecord.objects.get(id=record_id)
    print("doctors:", record.doctors.all())
    return render(request, 'record_detail.html', {'record': record})

def detail_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)  
    form = PatientForm(instance=patient)
    return render(request, 'detail_patient.html', {'patient': patient, 'form': form})

def get_role_and_permissions(user):
    role = getattr(user.userprofile.role, 'name', '').lower()
    role_obj = Role.objects.filter(name__iexact=role).first()
    permissions = Update.objects.filter(role=role_obj).first() if role_obj else None
    return role, permissions

# Patient Views

def show_patient(request):
    patients = Patient.objects.all()
    role, permissions = get_role_and_permissions(request.user)
    return render(request, "show_patient.html", {
        'patients': patients,
        'role': role,
        'permissions': permissions
    })

def edit_patient(request, pk):
    role, permissions = get_role_and_permissions(request.user)
    if not (permissions and permissions.edit_report):
        return HttpResponse("You do not have permission to edit patients.")
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('show_patient')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'edit_patient.html', {'form': form})

def delete_patient(request, pk):
    role, permissions = get_role_and_permissions(request.user)
    if not (permissions and permissions.delete_report):
        return HttpResponse("You do not have permission to delete patients.")
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('show_patient')
    return render(request, 'delete_patient.html', {'patient': patient})

def view_patient(request, pk):
    patients = Patient.objects.all()
    role, permissions = get_role_and_permissions(request.user)
    if not (permissions and permissions.view_report):
        return HttpResponse("You do not have permission to view patients.")
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'show_patient.html', {'patient': patient,'patients':patients})



def show_record(request):
    records = MedicalRecord.objects.all()
    role, permissions = get_role_and_permissions(request.user)
    return render(request, 'view_medical.html', {
        'records': records,
        'role': role,
        'permissions': permissions
    })

def view_medical_record(request, pk):
    records = MedicalRecord.objects.all()
    role, permissions = get_role_and_permissions(request.user)
    if not (permissions and permissions.view_report):
        return HttpResponse("You do not have permission to view records.")
    record = get_object_or_404(MedicalRecord, pk=pk)
    return render(request, 'view_medical.html', {'record': record,'records':records})

def edit_medical_record(request, pk):
    role, permissions = get_role_and_permissions(request.user)
    if not (permissions and permissions.edit_report):
        return HttpResponse("You do not have permission to edit records.")
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('show_record')
    else:
        form = MedicalRecordForm(instance=record)
    return render(request, 'medical.html', {'form': form})

def delete_medical_record(request, pk):
    role, permissions = get_role_and_permissions(request.user)
    if not (permissions and permissions.delete_report):
        return HttpResponse("You do not have permission to delete records.")
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('show_record')
    return render(request, 'record_del.html', {'record': record})