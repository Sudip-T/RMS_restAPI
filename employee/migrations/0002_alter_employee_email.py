# Generated by Django 5.0.1 on 2024-01-22 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="email",
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]