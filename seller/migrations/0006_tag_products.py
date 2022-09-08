# Generated by Django 4.1 on 2022-09-07 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0005_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='tag_products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_products', models.TextField(max_length=225)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='seller.product_det')),
            ],
            options={
                'db_table': 'tag_product',
            },
        ),
    ]
