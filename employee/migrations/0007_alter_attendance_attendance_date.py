# Generated by Django 5.0.1 on 2024-01-22 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0006_alter_attendance_clock_out"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="attendance_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
