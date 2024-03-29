# Generated by Django 4.2.6 on 2024-01-31 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('street_address', models.CharField(max_length=255)),
                ('town_city', models.CharField(max_length=150)),
                ('country_state', models.CharField(max_length=150, verbose_name='State')),
                ('delivery_instructions', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='DeliveryOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_name', models.CharField(max_length=100)),
                ('delivery_price', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Delivery Option',
                'verbose_name_plural': 'Delivery Options',
                'ordering': ('delivery_price',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oid', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=10, max_length=13, prefix='oid', unique=True, verbose_name='Order ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_option', models.CharField(choices=[('on_receive', 'On Receive'), ('paypal', 'PayPal')], default='on_receive', max_length=255)),
                ('billing_status', models.BooleanField(default=False, null=True)),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('out_for_delivery', 'Out for Delivery'), ('delivered', 'Delivered'), ('refund', 'Refund'), ('canceled', 'Canceled')], default='pending', max_length=50, verbose_name='Order status')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('delivery', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='checkout.deliveryoptions', verbose_name='delivery_options')),
                ('shipping_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='addresses', to='checkout.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='book.book')),
                ('book_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.booktype')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.booklanguage')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='checkout.order')),
            ],
            options={
                'verbose_name': 'Order item',
                'verbose_name_plural': 'Order items',
            },
        ),
    ]
