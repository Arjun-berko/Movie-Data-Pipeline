#  ETL Pipeline and Dashboard for Analysing Movie Data 

## Description
This project utilizes Python, Docker, and Apache Airflow to create an ETL pipeline, complemented by a Power BI dashboard for data analysis. The aim is to explore the influence of genres, runtime, release dates, and the production country on movie performance, as well as the interrelationships between these variables.

## Features
- An Apache Airflow-managed ETL pipeline for seamless orchestration (setup only, DAG implementation to be added soon).
- Box Office Mojo's scraping for top box office data.
- TMDb API integration for enriching scraped data.
- Data processing with Pandas for enhanced analytics after each extraction.
- PostgreSQL integration for data storage, managed with Docker Compose.
- Power BI dashboard for insightful visualization of movie data, provided separately to GITHUB.


## Workflow Overview
The ETL pipeline operates as follows:


1. **Containerization:**
   - Docker Compose is used to define and run multi-container Docker applications. With a single command, you can create and start all the services defined in the `docker-compose.yml` file, including Airflow and PostgreSQL.

2. **Data Extraction:**
   - `box_office_scraper.py`: Scans Box Office Mojo and retrieves data regarding the top-performing movies. This includes titles, rankings, and box office statistics.
   - `movie_api_caller.py`: Uses the titles extracted from cleaned Box Office Mojo data to query TMDb's API, fetching detailed movie data such as genres, runtime, and release dates.

2. **Data Transformation:**
   - `box_office_cleaner.py`: Cleans and preprocesses box office data, standardizing formats and resolving inconsistencies.
   - `movie_api_cleaner.py`: Processes TMDb data, aligning it with the schema designed for analytics purposes.

3. **Data Loading:**
   - `data_postgres_loader.py`: Takes the cleaned data and loads it into PostgreSQL, where it is structured into tables suitable for complex queries and analysis.

4. **Data Orchestration:**
   - Apache Airflow manages the ETL pipeline, ensuring that tasks are executed in the correct sequence and monitoring for any failures or retries.

5. **Data Visualization:**
   - Power BI Dashboard: Connects to the PostgreSQL database to present the data through interactive visualizations, enabling users to derive insights and trends from the movie performance metrics.

Once Airflow DAGs are setup, each script will be orchestrated by Airflow to run in the correct order, ensuring that the data flows smoothly from extraction to visualization.
Currently, this execution has to be done manually.


## Installation
1. Ensure Docker and Docker Compose are installed on your system. Refer to the [Docker installation guide](https://docs.docker.com/get-docker/) and [Docker Compose installation](https://docs.docker.com/compose/install/).
2. Clone the repository: `git clone https://github.com/Arjun-berko/Movie-Data-Pipeline.git`.
3. Navigate to the cloned directory.
4. Install dependencies: `pip install -r requirements.txt`.
5. Start services: `docker-compose up --build`.

## Accessing the Interfaces
- **Airflow**: After setup, open `http://localhost:8080` in a browser.
- **pgAdmin**: Access at `http://localhost:5050` with the credentials from `docker-compose.yml`.
- **Power BI**: Update the dashboard data by connecting to the PostgreSQL database using the host machine's IP address.

## Dependencies
- Apache Airflow 2.7.2
- PostgreSQL 13
- Docker (latest)
- Docker Compose (latest)
- Python 3.8+
- Python packages from `requirements.txt`

## Quick Start
- Initialize Airflow: `docker-compose up airflow-init`.
- Start the ETL pipeline: `docker-compose up -d`.
- Execute scripts in order: `box_office_scraper.py`, `box_office_cleaner.py`, `movie_api_caller.py`, `movie_api_cleaner.py`, `data_postgres_loader.py`. Ensure you insert your TMDb API key in `movie_api_caller.py`.


