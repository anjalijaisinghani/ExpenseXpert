# Generated by Django 5.1.3 on 2024-12-04 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='expenses',
            fields=[
                ('expense_id', models.AutoField(primary_key=True, serialize=False)),
                ('expense_name', models.CharField(max_length=100)),
                ('expense_amount', models.CharField(max_length=100)),
                ('expense_category', models.CharField(max_length=100)),
                ('expense_date', models.DateField()),
            ],
        ),
    ]
