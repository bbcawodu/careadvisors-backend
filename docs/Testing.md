# Writing and Running Tests README


## Running Tests

### Running Tests with output to the shell
python manage.py test

### Running Tests with output to text files
- stdout is the file into which the kernel writes its output and the process requesting it accesses the information from and stderr is the file into which all the exceptions are entered
python manage.py test > stdout.txt 2> stderr.txt

this command will create a test fixture that can be loaded within each test case and with setUpTestData(cls) but doesnt work with initial_data load
python3 manage.py dumpdata --exclude contenttypes.ContentType > 12-21-2016.json

-creating an empty migration
python manage.py makemigrations --empty <yourapp> --name load_intial_data