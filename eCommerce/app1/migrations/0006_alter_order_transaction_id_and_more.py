# Generated by Django 5.0.2 on 2024-03-05 11:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_product_avg_rating_product_total_ratings_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.PositiveIntegerField(blank=True, default=87375486617),
        ),
        migrations.AlterField(
            model_name='reviewofproduct',
            name='rating',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]