# Generated by Django 4.1.13 on 2024-08-11 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_invoice_invoice_id_alter_invoice_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]