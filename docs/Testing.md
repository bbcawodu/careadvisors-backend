# Writing and Running Tests README


## Running Tests

### Running Tests with output to the shell
python manage.py test

### Running Tests with output to text files
- stdout is the file into which the kernel writes its output and the process requesting it accesses the information from and stderr is the file into which all the exceptions are entered
python manage.py test > stdout.txt 2> stderr.txt

-command to print terminal history to text file
history > history_for_print.txt


### Loading test database data from migration
this command will create a test fixture that can be loaded within each test case and with setUpTestData(cls) but doesnt work with initial_data load
python3 manage.py dumpdata --exclude contenttypes.ContentType > 12-21-2016.json


this command will create a fixture with current data from the database which can be used to load data from migration
python3 manage.py dumpdata --exclude sessions.Session > 01-23-2017.json


-creating an empty migration
python manage.py makemigrations --empty <yourapp> --name load_intial_data

- fill empty migration file with the following
```
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


from django.core.management import call_command

fixture = '12-27-2016.json'


def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture)


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0032_auto_20161222_2106'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
```


# Command to load data to database from json file

python manage.py loaddata [file]


git update-index --assume-unchanged picbackend/wsgi.py

git update-index --no-assume-unchanged picbackend/wsgi.py

# Please enter a commit message to explain why this merge is necessary,especially if it merges an updated upstream into a topic branch

To solve this:

- press "i"
- write your merge message
- press "esc"
- write ":wq"
- then press enter
