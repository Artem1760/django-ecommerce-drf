# Generated by Django 4.2.6 on 2023-12-24 09:13

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=150)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('publication_date', models.DateField()),
                ('isbn', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', editable=False, length=13, max_length=25, prefix='isbn', unique=True)),
                ('regular_price', models.DecimalField(decimal_places=2, default=10, max_digits=10, verbose_name='Regular price')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Discount price')),
                ('is_sale', models.BooleanField(default=False)),
                ('cover', models.ImageField(blank=True, default='book_default.png', null=True, upload_to='book_covers')),
                ('description', ckeditor.fields.RichTextField(blank=True, db_index=True, default='This is the book', null=True)),
                ('specification', ckeditor.fields.RichTextField(blank=True, default='Book Specification', null=True)),
                ('digital', models.BooleanField(blank=True, default=False, null=True)),
                ('quantity', models.IntegerField(blank=True, default='25', null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('num_pages', models.PositiveIntegerField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='book.author')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
                'ordering': ('-created_date', 'title'),
            },
        ),
        migrations.CreateModel(
            name='BookLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Book language',
                'verbose_name_plural': 'Book languages',
            },
        ),
        migrations.CreateModel(
            name='BookType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Book type',
                'verbose_name_plural': 'Book types',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='FilterPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(choices=[('Under $25', 'Under $25'), ('$25 to $50', '$25 to $50'), ('$50 to $100', '$50 to $100'), ('$100 to $200', '$100 to $200'), ('$200 & Above', '$200 & Above')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
            ],
            options={
                'verbose_name': 'Publisher',
                'verbose_name_plural': 'Publishers',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='BookReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star_rating', models.PositiveIntegerField(choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')])),
                ('review', models.CharField(max_length=255)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Book Review',
                'verbose_name_plural': 'Book Reviews',
            },
        ),
        migrations.CreateModel(
            name='BookImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='default_avatar.png', null=True, upload_to='book_images')),
                ('is_feature', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_images', to='book.book')),
            ],
            options={
                'verbose_name': 'Book image',
                'verbose_name_plural': 'Book images',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='book_type',
            field=models.ManyToManyField(related_name='types', to='book.booktype'),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='book.category'),
        ),
        migrations.AddField(
            model_name='book',
            name='filter_price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.filterprice'),
        ),
        migrations.AddField(
            model_name='book',
            name='languages',
            field=models.ManyToManyField(related_name='languages', to='book.booklanguage'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='publisher', to='book.publisher'),
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='book',
            name='users_wishlist',
            field=models.ManyToManyField(blank=True, related_name='users_wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
