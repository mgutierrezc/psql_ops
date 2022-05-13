import pandas as pd
import time
from datetime import date, datetime
import keyword
import json


# List of reserved words obtained from https://www.postgresql.org/docs/7.3/sql-keywords-appendix.html


def create_diagram(table_name, dataframe, primary_keys = ["WorkerId", "round_num"]):
    """
    Generate and create a psql table on the project server
    
    Input:
    * table_name: name of the psql table to be generated
    * dataframe: pandas dataframe containing the variable names
    * primary_keys: list of variable names that should be treated as primary keys
      (NOTE: limited error checking is done on these names)
    
    
    """
    
    # # Dictionary to convert data types from dataframe into postgres datatypes
    # data_types = {'int': 'int', 'str': 'varchar', 'datetime': 'datetime', 'float': 'double', 'double': 'double'}
    
    
    # List of reserved words in PostgreSQL (btained from https://www.postgresql.org/docs/7.3/sql-keywords-appendix.html)
    keywords_json_file = open("postgres_reserved_keywords.json")
    keywords_json = json.load(keywords_json_file)
    reserved_words_psql = keywords_json[0]['reserved_keywords']
    
    
    # Store field names and their respective types
    field_type_pairs = []
    
    # Store variable names that were found to be keywords and subsequently modified
    changed_varnames = []
    
    # Store the number of primary keys seen for error chekcing
    primary_key_count = 0
    
    # Iterate through dataframe and extract field name and type
    for column in dataframe:
        reserved = False
        # Check if the variable name is a reserved keyword
        if (keyword.iskeyword(column)) or (column.upper() in reserved_words_psql):
            changed_varnames.append(column)
            reserved = True
            
        is_primary_key = False
        if (primary_keys != None) and (column in primary_keys):
            is_primary_key = True
            primary_key_count += 1
            
        if reserved == False:
            pair = f"\"{column.lower()}\" "   # Names of variables should be in lowercase
        else:
            pair = f"\"{column.lower()}_var\" "   # Add "_var" to reserved variable name to make it usable
 
        
        # Find the appropriate postgres data type for the variable
        if(("object" in str(dataframe[column].dtype)) or ("str" in str(dataframe[column].dtype))):
            pair += "varchar"
        elif(("float" in str(dataframe[column].dtype))or ("double" in str(dataframe[column].dtype))):
            pair += "double precision"
        elif("int" in str(dataframe[column].dtype)):
            pair += "int"
        elif(("date" in str(dataframe[column].dtype)) or ("time" in str(dataframe[column].dtype))):
            pair += "timestamp with time zone"
        

            
        # Add PRIMARY KEY in case this variable plays that role
        if is_primary_key and (len(primary_keys) == 1):
            pair += " PRIMARY KEY"
        
        # Add string with variable name and type to list
        field_type_pairs.append(pair)
        
    
    # Error checking the primary key values given by comparing the number expected and actually found
    if (primary_keys != None) and (len(primary_keys) != primary_key_count):
        raise ValueError(f"{len(primary_keys) - primary_key_count} of the primary keys given were not found in the dataframe or were reserved keywords")
    
    
    
    # Start creating the string for the command
    diagram_creator = f'CREATE TABLE "{table_name}" (\n'

    # Use a default primary key if no argument was given
    if primary_keys == None:
        diagram_creator +=   '  "id_unico" INTEGER PRIMARY KEY,\n'
    
    
    # Join all variable-type pairs into a single list and add them to the command
    fields_listed = ",\n  ".join(field_type_pairs)
    if (primary_keys != None) and (len(primary_keys) > 1):
        diagram_creator += f"  {fields_listed}, \n"
    else:
        diagram_creator += f"  {fields_listed} \n"
       
    # If there are 2 or more PRIMARY KEY variables, indicate them as a list at the end
    if (primary_keys != None) and (len(primary_keys) > 1):
        # First convert the variables to lowercase
        lowercase_primary_keys = []
        for pk in primary_keys:
            lowercase_primary_keys.append(pk.lower())
        pk_string = ", ".join(lowercase_primary_keys)
        diagram_creator += f"  PRIMARY KEY ({pk_string})\n"

    diagram_creator += ");"
    
    # Print the variable names that were reserved keywords
    changed_varnames_str = ",\n ".join(changed_varnames)    
    print(f"Variable names that were found to be keywords and subsequently modified by adding _var: {changed_varnames_str}\n\n")
    
    
    return diagram_creator
    
    
    