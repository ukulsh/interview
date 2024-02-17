# Generated by Django 5.0.2 on 2024-02-17 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='processed',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='reserved_on',
            field=models.DateTimeField(db_index=True),
        ),
    ]
