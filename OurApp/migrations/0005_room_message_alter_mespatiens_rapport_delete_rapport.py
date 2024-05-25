# Generated by Django 5.0.6 on 2024-05-25 09:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OurApp', '0004_remove_rendezvous_rapport_rapport_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('reponse', models.CharField(max_length=255)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OurApp.room')),
            ],
        ),
        migrations.AlterField(
            model_name='mespatiens',
            name='rapport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OurApp.room'),
        ),
        migrations.DeleteModel(
            name='Rapport',
        ),
    ]
