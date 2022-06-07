import pandas as pd
import time
from sqlalchemy import create_engine
import psycopg2


def upload_to_psql(file_path, user, passw, host, db_name, table_name, option):
    """
    Uploads data file to psql
    Supported formats: csv, xlsx
    Input: Psql user, password, host name, database name, table name,
    upload option (strings)
    Output: None
    """

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    print(f"Step 1 completed: File {file_path} read")

    conn_string = f"postgresql://{user}:{passw}@{host}/{db_name}"
    conn = create_engine(conn_string, pool_pre_ping=True)
    print(f"Step 2 completed: Engine created")

    start_time = time.time()
    print(f"Step 3 completed: Timer started")

    df.to_sql(table_name, conn, method='multi', if_exists=option, index=False)
    print("Step 4 (Final) completed: --- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    import os

    file_path = input("Input your CSV file path: ")
    user = os.environ.get("wb_psql_user")
    password = os.environ.get("wb_psql_pwd")
    host = os.environ.get("wb_psql_host_url")
    db_name = "otree_audio_covering"
    table_name = input("Input your desired table name: ")
    option = input("Choose how you want to upload the data (append or replace): ")

    upload_to_psql(file_path, user, password, host, db_name, table_name, option)


    
