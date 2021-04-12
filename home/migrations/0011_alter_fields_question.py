# Generated by Django 3.1.6 on 2021-04-11 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_merge_20210410_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='home.book'),
        ),
        migrations.AlterField(
            model_name='question',
            name='sub_subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='home.sub_subject'),
        ),
    ]
