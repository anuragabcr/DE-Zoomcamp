#!/usr/bin/env python
# coding: utf-8

from sqlalchemy import create_engine
import pandas as pd
from time import time
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")

    # engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    for i, df in enumerate(df_iter):
        t_start = time()
        
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name="yellow_taxi_data", con=engine, if_exists="append", index=False)
        
        t_end = time()
        print(f"✅ Inserted chunk {i+1} ({len(df)} rows) in {t_end - t_start:.2f} seconds")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV data into postgres")

    parser.add_argument("--user", help="name for the postgres")
    parser.add_argument("--password", help="passowrd for the postgres")
    parser.add_argument("--host", help="host for the postgres")
    parser.add_argument("--port", help="port for the postgres")
    parser.add_argument("--db", help="db name for the postgres")
    parser.add_argument("--table_name", help="table name for the postgres")
    parser.add_argument("--url", help="csv file url")

    args = parser.parse_args()

    main(args)

