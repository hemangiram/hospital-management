from django.db import models

# Create your models here.
class Service(models.Model):
    icon_class = models.CharField(max_length=100, help_text="Enter icon class e.g. 'fas fa-heartbeat'")
 # Requires media config
    name = models.CharField(max_length=100)
    description = models.TextField()
   

    def __str__(self):
        return self.name
    

class Department(models.Model):
    name = models.CharField(max_length=100)  # e.g., Cardiology
    image = models.ImageField(upload_to='departments/')  # Requires media config
    short_description = models.TextField()
    long_description = models.TextField()

    def __str__(self):
        return self.name