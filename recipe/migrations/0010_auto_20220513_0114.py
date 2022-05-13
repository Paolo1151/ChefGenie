# Generated by Django 4.0.3 on 2022-05-12 17:14

from django.db import migrations

import os

def insert_test_data(apps, schema_editor):
    for table in ['mealmade', 'review']:
        with open(os.path.join(os.path.dirname(__file__), 'testing_scripts', f'insert_testing_{table}.sql')) as insert_query:
            schema_editor.execute(insert_query.read())

def delete_test_data(apps, schema_editor):
    for table in ['mealmade', 'review']:
        schema_editor.connection.execute(f"TRUNCATE recipe_{table};")


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0009_auto_20220502_2111'),
    ]

    operations = [
        migrations.RunPython(code=insert_test_data, reverse_code=delete_test_data)
    ]
