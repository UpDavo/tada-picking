# Generated by Django 4.1.13 on 2024-07-10 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='product_photo',
            field=models.ImageField(blank=True, null=True, upload_to='product_photos/'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='description',
            field=models.CharField(default='Ninguno', max_length=150),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('awaiting_approval', 'Esperando Aprobación'), ('approved', 'Aprobado'), ('approved_but_incomplete', 'Aprobado con Detalle')], default='awaiting_approval', max_length=30),
        ),
    ]
