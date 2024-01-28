# Generated by Django 5.0.1 on 2024-01-23 10:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0013_alter_leaveapproval_leave_status_note_and_more"),
        ("inventory", "0006_remove_storerequest_collected_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="storerequest",
            name="requested_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="store_requests_requestedby",
                to="employee.employee",
            ),
        ),
    ]