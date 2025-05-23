# Generated by Django 5.2 on 2025-05-06 16:02

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0011_reportpost_timestamp_alter_reportpost_post_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportuser',
            name='user',
        ),
        migrations.AddField(
            model_name='reportuser',
            name='reported_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports_received', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reportuser',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='reportpost',
            name='reason',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='reportpost',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_reports_made', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reportuser',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reports_made', to=settings.AUTH_USER_MODEL),
        ),
    ]
