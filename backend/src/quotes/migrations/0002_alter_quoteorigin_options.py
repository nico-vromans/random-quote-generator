# Generated by Django 5.1.5 on 2025-01-19 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quoteorigin',
            options={'ordering': ('api_client_key', 'url'), 'verbose_name': 'Origin', 'verbose_name_plural': 'Origins'},
        ),
    ]
