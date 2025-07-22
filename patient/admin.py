from django.contrib import admin
from .models import Patient
from .models import MedicalRecord,Appointment,UserProfile,Billing,Ward,Role,Module,Doctor
from .models import Update
# Register your models here.

admin.site.register(Appointment)
admin.site.register(UserProfile)
admin.site.register(Billing)
admin.site.register(Ward)
admin.site.register(Role)
admin.site.register(Module)
admin.site.register(Doctor)
admin.site.register(Update)


from django.contrib import admin
from .models import Patient, MedicalRecord

class PatientAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(doctors=request.user)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'doctors' and not request.user.is_superuser:
            kwargs['queryset'] = kwargs['queryset'].filter(id=request.user.id)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

class MedicalRecordAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(doctors=request.user)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'doctors' and not request.user.is_superuser:
            kwargs['queryset'] = kwargs['queryset'].filter(id=request.user.id)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Patient, PatientAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
