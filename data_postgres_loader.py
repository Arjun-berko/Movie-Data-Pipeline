import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def read_csv_file(file_path):
    """
    Read a CSV file into a DataFrame.

    :param file_path: Path to the CSV file.
    :return: A pandas DataFrame.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        print(f"No data: {file_path}")
    except pd.errors.ParserError:
        print(f"Error parsing data: {file_path}")
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
    return None

def to_sql_with_error_handling(df, table_name, engine):
    """
    Write records stored in a DataFrame to a SQL database.

    :param df: DataFrame to be written to the database.
    :param table_name: Name of the target database table.
    :param engine: SQLAlchemy engine instance.
    """
    if df is not None:
        try:
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"Data loaded into {table_name} successfully.")
        except SQLAlchemyError as e:
            print(f"Error writing to database: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Read the cleaned data from CSV
    uk_bo_data = read_csv_file('box_office_data_cleaned/box_office_cleaned_uk.csv')
    us_bo_data = read_csv_file('box_office_data_cleaned/box_office_cleaned_usa.csv')
    api_data = read_csv_file('api_moviedata/api_moviedata_cleaned.csv')

    # Database connection parameters
    DATABASE = {
        'dbname': 'airflow',
        'user': 'airflow',
        'password': 'airflow',
        'host': 'localhost',
        'port': 5432
    }

    # Create an SQLAlchemy engine
    engine = None
    try:
        engine = create_engine(f"postgresql+psycopg2://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['dbname']}")
    except SQLAlchemyError as e:
        print(f"Database connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while connecting to the database: {e}")

    # Load data to PostgreSQL
    if engine:
        to_sql_with_error_handling(uk_bo_data, 'uk_box_office', engine)
        to_sql_with_error_handling(us_bo_data, 'usa_boxoffice', engine)
        to_sql_with_error_handling(api_data, 'individual_movie_details', engine)
