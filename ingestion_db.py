import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename='logs/ingestion_db.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

engine = create_engine('sqlite:///inventory.db')

for file in os.listdir('data'):
    if '.csv' in file:
        df = pd.read_csv('data/' + file)
        print(df.shape)

def ingest_db(df, table_name, engine):
    '''this function will ingest the dataframe into database table'''
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

chunk_size = 100000

def load_raw_data():
    '''this function will load the CSVs as dataframe and ingest into db'''
    start = time.time()
    for file in os.listdir('data'):
        if file.endswith('.csv'):
            logging.info(f'Ingesting{file} in db')
            for chunk in pd.read_csv('data/' + file, chunksize=chunk_size):
                ingest_db(chunk, file[:-4], engine)
    end = time.time()
    total_time = (end - start)/60
    logging.info('---------Data ingestion completed---------')
    logging.info(f'\nTotal time taken: {total_time} minutes')

if __name__ == '__main__':
    load_raw_data()
    print('Data ingestion completed')