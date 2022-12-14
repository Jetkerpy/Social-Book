# Generated by Django 4.1.2 on 2022-10-17 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_book_is_saved'),
        ('comment', '0001_initial'),
        ('likeordislike', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dislike',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_dislikes', to='comment.parentcomment'),
        ),
        migrations.AddField(
            model_name='like',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='comment.parentcomment'),
        ),
        migrations.AlterField(
            model_name='dislike',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dislike_book', to='book.book'),
        ),
        migrations.AlterField(
            model_name='like',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='like_book', to='book.book'),
        ),
    ]
