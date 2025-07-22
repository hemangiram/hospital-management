# patient/apps.py

from django.apps import AppConfig

class PatientConfig(AppConfig):
    name = 'patient'

    def ready(self):
        print("Patient app is ready")
        import patient.signals # Ensure signals are imported when the app is ready
        print("Signals for Patient app are set up")
        # Additional setup can be done here if needed       
















































