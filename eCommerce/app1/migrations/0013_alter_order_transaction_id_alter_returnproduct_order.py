# Generated by Django 5.0.2 on 2024-03-08 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_returnproduct_order_alter_order_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.PositiveIntegerField(blank=True, default=9254571991),
        ),
        migrations.AlterField(
            model_name='returnproduct',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app1.order'),
        ),
    ]
