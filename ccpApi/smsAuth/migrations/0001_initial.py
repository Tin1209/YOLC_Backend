# Generated by Django 3.2.6 on 2021-09-24 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auth',
            fields=[
                ('phone_number', models.CharField(max_length=11, primary_key=True, serialize=False, verbose_name='휴대폰 번호')),
                ('auth_number', models.IntegerField(verbose_name='인증 번호')),
            ],
            options={
                'db_table': 'smsauth',
            },
        ),
    ]
