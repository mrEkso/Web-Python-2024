# Generated by Django 5.0.6 on 2024-05-22 00:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('financial_exchange', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='account',
        ),
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='account_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='account_from', to='financial_exchange.account'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='account_to',
            field=models.ForeignKey(default=500, on_delete=django.db.models.deletion.CASCADE, related_name='account_to',
                                    to='financial_exchange.account'),
            preserve_default=False,
        ),
    ]
