# Generated by Django 4.2.23 on 2025-07-22 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0009_doctor_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='desc',
            field=models.TextField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
