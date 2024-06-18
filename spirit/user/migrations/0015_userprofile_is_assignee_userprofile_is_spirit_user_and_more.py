# Generated by Django 4.2.1 on 2023-08-21 04:30

from django.db import migrations, models
import spirit.core.storage
import spirit.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_user', '0014_alter_userprofile_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_assignee',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_spirit_user',
            field=models.BooleanField(default=True, verbose_name='spirit user'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, max_length=255, storage=spirit.core.storage.select_storage, upload_to=spirit.user.models.avatar_path, verbose_name='avatar'),
        ),
    ]