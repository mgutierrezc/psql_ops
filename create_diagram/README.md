# README

## HOW TO USE:
Change the variables in database.ini to create a table in the
intended database with a particular username and password
(the database.ini file must be created by the user; see
instructions below).

In select.py, choose whether to read from a .xlsx or a .dta
file, and comment out the option that is not used.
Provide the appropriate file path for reading the database.
Make sure to change the arguments of create_diagram to give
the name of the table to be created, and to indicate to the 
function which (if any) variable names should be used as 
PRIMARY KEY (if no argument is given, the function adds a default
identifier).

To run the program, type "python connect.py" in the relevant
directory.

### Structure for database.ini:
[postgresql]
host=
database=
user=
password=


## DETAILS:
create_diagram.py detects if any of the variable names are 
reserved keywords in Python or Postgres. If so, it adds
"_var" at the end of the variable name, and at the end it prints
a list with all the variables that were using reserved keywords.

### Python connection to PostgreSQL largely based on this tutorial:
https://www.postgresqltutorial.com/postgresql-python/connect/
