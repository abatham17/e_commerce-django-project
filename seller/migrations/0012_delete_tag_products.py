# Generated by Django 4.1 on 2022-09-07 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0011_alter_tag_products_t_products'),
    ]

    operations = [
        migrations.DeleteModel(
            name='tag_products',
        ),
    ]
