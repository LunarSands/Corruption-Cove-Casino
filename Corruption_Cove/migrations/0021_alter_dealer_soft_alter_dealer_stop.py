# Generated by Django 5.0.2 on 2024-03-17 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Corruption_Cove', '0020_alter_bank_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealer',
            name='soft',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='stop',
            field=models.IntegerField(default=17),
        ),
    ]