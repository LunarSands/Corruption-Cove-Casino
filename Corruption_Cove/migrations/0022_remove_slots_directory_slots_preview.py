# Generated by Django 5.0.1 on 2024-03-21 20:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Corruption_Cove", "0021_alter_dealer_soft_alter_dealer_stop"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="slots",
            name="directory",
        ),
        migrations.AddField(
            model_name="slots",
            name="preview",
            field=models.ImageField(
                default="/media/images/slots/Classic.png", upload_to=""
            ),
            preserve_default=False,
        ),
    ]