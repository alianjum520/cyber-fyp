# Generated by Django 4.0 on 2023-04-02 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0004_alter_like_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='tweet',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='social_network.tweet'),
        ),
    ]
