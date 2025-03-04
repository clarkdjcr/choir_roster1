# Generated by Django 4.2.9 on 2025-02-26 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RosterApplication', '0002_chatmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnreadMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RosterApplication.chatmessage')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RosterApplication.choirmember')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
