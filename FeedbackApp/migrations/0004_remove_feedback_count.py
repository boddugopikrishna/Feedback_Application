# Generated by Django 3.0.1 on 2019-12-30 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FeedbackApp', '0003_remove_feedback_data_feedbackid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='count',
        ),
    ]
