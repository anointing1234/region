# Generated by Django 5.2 on 2025-05-09 03:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(default='Default Bank', max_length=255)),
                ('branch_name', models.CharField(default='Default Branch', max_length=255)),
                ('account_number', models.CharField(default='0000000000', max_length=20)),
                ('account_holder', models.CharField(default='Default Account Holder', max_length=255)),
                ('swift_code', models.CharField(default='SWIFT000', max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('reset_code', models.CharField(max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('product_category', models.CharField(choices=[('Amplifiers', 'Amplifiers'), ('Digital', 'Digital'), ('Loudspeakers', 'Loudspeakers'), ('Mixer Console', 'Mixer Console'), ('Turntables', 'Turntables')], max_length=50)),
                ('product_type', models.CharField(choices=[('Audio Equipment', 'Audio Equipment'), ('Accessories', 'Accessories'), ('Components', 'Components')], max_length=50)),
                ('product_tag', models.CharField(blank=True, choices=[('Featured Products', 'Featured Products'), ('Bestsellers', 'Bestsellers'), ('Popular Categories', 'Popular Categories'), ('New Arrivals', 'New Arrivals'), ('Sale', 'Sale'), ('Top Rated', 'Top Rated')], max_length=50, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reviews_in_stars', models.DecimalField(decimal_places=1, default=0.0, max_digits=2)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('shipping_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, editable=False, max_length=20, unique=True)),
                ('street_address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('under_review', 'Under Review'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='under_review', max_length=20)),
                ('product_details', models.TextField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shipping_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order_image', models.ImageField(blank=True, null=True, upload_to='order_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('delivery_date_start', models.DateField(blank=True, null=True)),
                ('delivery_date_end', models.DateField(blank=True, null=True)),
                ('bank_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.bankdetails')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('shipping_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WrittenReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stars', models.PositiveIntegerField(default=0)),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='reviews/')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='written_reviews', to='accounts.product')),
            ],
        ),
    ]
