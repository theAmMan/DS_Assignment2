# Generated by Django 4.1.7 on 2023-03-05 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('distqueue', '0004_remove_consumer_subscriptions_remove_logmessage_prod_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consumer',
            old_name='subscription',
            new_name='subscriptions',
        ),
    ]