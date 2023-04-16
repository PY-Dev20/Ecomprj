# Generated by Django 4.1.7 on 2023-04-03 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_product_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='core.vendor'),
        ),
    ]
