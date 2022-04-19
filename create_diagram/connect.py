#!/usr/bin/python
import psycopg2
from config import config
from create_diagram import create_diagram
import pandas as pd
import time
from datetime import date, datetime
import keyword

def connect():
    """ 
    Connect to the PostgreSQL database server and create table using
    create_diagram 
    """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('Creating table using create_diagram...')
        
        # CHOOSE ONE, COMMENT OUT THE OTHER
        # if excel file (.xlsx), use pd.read_excel
        df = pd.read_excel("FILEPATH HERE" )
        # if .dta file, use pd.read_stata
        # stata1 = pd.read_stata("FILEPATH HERE", convert_categoricals=False) # Note the convert_categoricals=False
        
        command = create_diagram("TABLE_NAME HERE", df, primary_keys = None)
        
        
        test_command = """
        CREATE TABLE test2 (
            test_id2 int PRIMARY KEY,
            test_name2 varchar
        );
        """
        
        cur.execute(command)
        

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
	
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Attempt failed.")
        raise
        print(error)
    finally:
        if conn is not None:
            conn.commit() 
            conn.close()
            # close the communication with the PostgreSQL
            cur.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()