# Generated by Django 4.1.2 on 2022-10-20 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_parentcomment_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='parentcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parents_comment', to='comment.parentcomment'),
        ),
    ]
