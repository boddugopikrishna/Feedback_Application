# Generated by Django 3.0.1 on 2019-12-30 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FeedbackApp', '0002_feedback_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback_data',
            name='feedbackId',
        ),
    ]
