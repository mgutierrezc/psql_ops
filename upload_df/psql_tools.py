import pandas as pd
import time
from sqlalchemy import create_engine
import psycopg2



def upload_to_psql(file_path, user, passw, host, db_name, table_name, option):
    """
    Uploads csv data to psql

    Input: Psql user, password, host name, database name, table name,
    upload option (strings)
    Output: None
    """

    df=pd.read_csv(file_path)
    print(f"Step 1 completed: File {file_path} read")

    conn_string = f"postgresql://{user}:{passw}@{host}/{db_name}"
    conn = create_engine(conn_string, pool_pre_ping=True)
    print(f"Step 2 completed: Engine created")

    start_time = time.time()
    print(f"Step 3 completed: Timer started")
    
    df.to_sql(table_name, conn, method='multi', if_exists=option, index=False)
    print("Step 4 (Final) completed: --- %s seconds ---" % (time.time() - start_time))


def psql_query(user, passw, host, db_name):
    """
    Allows select 

    Input: Psql user, password, host name, database name, table name,
    upload option (strings)
    Output: None
    """

    conn = psycopg2.connect(dbname=db_name, user=user, password=passw, host=host)
    print(f"Step 1 completed: Connection string")

    cur = conn.cursor()
    query = input("Input your query: ")
    cur.execute(query)
    
    for obs in cur:
        print(obs)


if __name__ == '__main__':
    import os

    option_type = input("Input the DB type you want to use ('wb' or 'alegra'): ")

    if option_type == "wb":
        user = os.environ.get("wb_psql_user")
        password = os.environ.get("wb_psql_pwd")
        host = os.environ.get("wb_psql_host_url")
        db_name = "peru_amag_ii"

    elif option_type == "alegra":
        user = os.environ.get("ALEGRA_DB_USER")
        password = os.environ.get("ALEGRA_DB_PASSWORD")
        host = os.environ.get("ALEGRA_DB_HOST")
        db_name = os.environ.get("ALEGRA_DB_NAME")

    psql_query(user, password, host, db_name)

    # file_path = input("Input your CSV file path: ")

    
    # table_name = input("Input your desired table name: ")
    # option = input("Choose how you want to upload the data (append or replace): ")

    # upload_to_psql(file_path, user, password, host, db_name, table_name, option)

    