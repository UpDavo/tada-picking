# Generated by Django 4.1.13 on 2024-08-10 23:58

import core.utils.storage_backend
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_invoice_product_photo_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='picker_ci',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='picker_name',
        ),
        migrations.AddField(
            model_name='client',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='client',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='core.client'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='invoice',
            name='picker',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='product_photo',
            field=models.ImageField(blank=True, default='default.jpg', null=True, storage=core.utils.storage_backend.PublicUploadStorage(), upload_to='invoice_photos/'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.store'),
        ),
    ]
