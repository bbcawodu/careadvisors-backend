# Writing and Running Tests README


## Running Tests

### Running Tests with output to the shell
python manage.py test

### Running Tests with output to text files
- stdout is the file into which the kernel writes its output and the process requesting it accesses the information from and stderr is the file into which all the exceptions are entered
python manage.py test > stdout.txt 2> stderr.txt