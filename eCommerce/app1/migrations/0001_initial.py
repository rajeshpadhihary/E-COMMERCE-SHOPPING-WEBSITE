# Generated by Django 5.0.2 on 2024-03-04 16:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('selling_price', models.FloatField()),
                ('discounted_price', models.FloatField()),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('T-Shirts', 'T-Shirts'), ('Shirts', 'Shirts'), ('Jeans', 'Jeans'), ('Shoes', 'Shoes'), ('Watches', 'Watches')], max_length=50)),
                ('forgender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Unisex', 'Unisex')], max_length=50)),
                ('product_image', models.ImageField(upload_to='product')),
            ],
        ),
        migrations.CreateModel(
            name='CreditCardDetailsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_on_card', models.CharField(max_length=100)),
                ('card_number', models.CharField(max_length=16)),
                ('expiry_date_month', models.CharField(max_length=2)),
                ('expiry_date_year', models.CharField(max_length=4)),
                ('cvv', models.CharField(max_length=3)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField(default='**********')),
                ('city', models.CharField(max_length=100)),
                ('zipcode', models.IntegerField(blank=True, null=True)),
                ('state', models.CharField(choices=[('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh', 'Arunachal Pradesh'), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chandigarh', 'Chandigarh'), ('Delhi', 'Delhi'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Jammu and Kashmir', 'Jammu and Kashmir'), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Pondicherry', 'Puduchery'), ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttarakhand', 'Uttarakhand'), ('Uttar Pradesh', 'Uttar Pradesh'), ('West Bengal', 'West Bengal')], max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_for_profile', models.CharField(blank=True, max_length=100, null=True)),
                ('about', models.CharField(max_length=400)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='userprofileimages')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DebitCardDetailsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_on_card', models.CharField(max_length=100)),
                ('card_number', models.CharField(max_length=16)),
                ('expiry_date_month', models.CharField(max_length=2)),
                ('expiry_date_year', models.CharField(max_length=4)),
                ('cvv', models.CharField(max_length=3)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.CharField(max_length=400)),
                ('quantity', models.CharField(max_length=400)),
                ('total_price', models.FloatField(default=1)),
                ('cash_on_delivery', models.BooleanField(default=False)),
                ('debit_card', models.BooleanField(default=False)),
                ('credit_card', models.BooleanField(default=False)),
                ('transaction_id', models.PositiveIntegerField(blank=True, default=75805480287)),
                ('order_status', models.BooleanField(default=False)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.customeraddress')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.product')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
