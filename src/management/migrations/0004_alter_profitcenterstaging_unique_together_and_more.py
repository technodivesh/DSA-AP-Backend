# Generated by Django 4.0.1 on 2022-09-30 05:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_remove_profitcenterstaging_is_deleted_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='profitcenterstaging',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='customergroup',
            name='end_date',
            field=models.DateTimeField(blank=True, db_column='EndDate', default=None, null=True, verbose_name='EndDate'),
        ),
        migrations.AlterField(
            model_name='customergroup',
            name='start_date',
            field=models.DateTimeField(db_column='StartDate', default=django.utils.timezone.now, verbose_name='StartDate'),
        ),
        migrations.AlterField(
            model_name='employeeauthdc',
            name='end_date',
            field=models.DateTimeField(blank=True, db_column='EndDate', default=None, null=True, verbose_name='EndDate'),
        ),
        migrations.AlterField(
            model_name='employeeauthdc',
            name='start_date',
            field=models.DateTimeField(db_column='StartDate', default=django.utils.timezone.now, verbose_name='StartDate'),
        ),
        migrations.AlterField(
            model_name='employeeauthpc',
            name='end_date',
            field=models.DateTimeField(blank=True, db_column='EndDate', default=None, null=True, verbose_name='EndDate'),
        ),
        migrations.AlterField(
            model_name='employeeauthsc',
            name='end_date',
            field=models.DateTimeField(blank=True, db_column='EndDate', default=None, null=True, verbose_name='EndDate'),
        ),
    ]
