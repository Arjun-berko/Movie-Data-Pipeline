import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Read the cleaned data from CSV
uk_bo_data= pd.read_csv('box_office_data_cleaned/box_office_cleaned_uk.csv')
us_bo_data= pd.read_csv('box_office_data_cleaned/box_office_cleaned_usa.csv')
api_data=pd.read_csv('api_moviedata/api_moviedata_cleaned.csv')



# Database connection parameters
DATABASE = {
    'dbname': 'test_db',
    'user': 'root',
    'password': 'root',
    'host': 'localhost', # 'localhost'
    'port': 5432
}

# Create an SQLAlchemy engine
engine = create_engine(f"postgresql+psycopg2://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['dbname']}")


# Load data to PostgreSQL
uk_bo_data.to_sql('uk_box_office', engine, if_exists='replace', index=False)  # 'movies' is the table name. 'replace' will replace the table if it exists.
us_bo_data.to_sql('usa_boxoffice', engine, if_exists='replace', index=False)  # 'movies' is the table name. 'replace' will replace the table if it exists.
api_data.to_sql('individual_movie_details', engine, if_exists='replace', index=False)  # 'movies' is the table name. 'replace' will replace the table if it exists.


