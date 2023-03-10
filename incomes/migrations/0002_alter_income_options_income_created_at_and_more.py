# Generated by Django 4.1.2 on 2023-03-10 08:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('incomes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='income',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AddField(
            model_name='income',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='income',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]