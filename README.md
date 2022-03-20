# Sparkify Analytics Database

This database was created as a means to give the analytics team a simple way to access the song play data initially stored in json files. This will enable the company to query the database and answer questions that will help understand how the users are currently using the streaming app. A star schema has been implemented so that queries on the data are fast and intuitive and easy to do whether that is through python or sql directly.

## Project structure

The project has been created with the following structure:

```bash
├── README.md
├── create_tables.py
├── data
│   ├── log_data
│   └── song_data 
├── etl.ipynb
├── etl.py
├── sql_queries.py
└── test.ipynb
```

- create_tables.py: Script that deletes the database and tables if they already exists and then recreates the database with all the tables 
- etl.ipynb: Developmental notebook. Used to test the creation of the database and the basic insert commands.
- etl.py: Production script that inserts the data into the star schema
- sql_queries.py: Saved queries for the creation, insertion and deletion of the database
- test.ipynb: SQL queries to check the structure of the database
- data: Database raw data in json files.

## Usage

2 datasets, log_data and  song_data, have been migrated trough and ETL process to the PostgreSQL database.

To build the database please execute the following commands in the terminal:

```bash
python create_tables.py
python etl.py
```

The latter script will show the progress of the insertion process.

If any problems are encountered it is recommended to run the development notebooks (etl.ipynb, test.ipynb) to debug the code. Always run the create_tables.py before running these scripts. Remember to restart the kernel on both notebooks before running create_tables.py.

## Star Schema

A star schema was implemented in order to make queries about the usage of the streaming app as simple as possible. With the implemented schema it is simpler to do queries based on the preferences of the users:

Where are the most loyal users?

```sql
sql SELECT location, COUNT(location) FROM songplays GROUP BY location ORDER BY count DESC LIMIT 5
```

Who are the most loyal users?

```sql
sql SELECT songplays.user_id, users.first_name, users.last_name, COUNT(songplays.user_id) 
FROM (songplays JOIN users ON users.user_id = songplays.user_id) 
GROUP BY songplays.user_id, users.first_name, users.last_name 
ORDER BY COUNT(songplays.user_id) DESC;
```

Which month and where are the most frequent users?

```sql
sql SELECT month, location, COUNT(location) 
FROM (songplays JOIN time ON time.start_time=songplays.start_time) 
GROUP BY location, month 
ORDER BY count DESC;
```
and many others!

Some queries can be performed directly on the songplays table while others involving user, song, time and artist data are only one join away.

![Alt text](https://raw.githubusercontent.com/Davidcparrar/nanodegree-datamodelingpostgres/main/PostgresStarSchemaSparkify.svg)

Based on this design the ETL implementation was straightforward:

- Read log files and song files metadata
- Process some columns on the data like timestamps and datetime.
- Extract relevant data for each table
- Insert data on each table

The python libraries psycopg2 and pandas where used in most of the implementation.

## Docker

A docker compose file is provided to run a Postgres Database locally for developing purposes. 

```bash
docker-compose up
```

A PgAdmin service is also included to help the user interact with the database. When creating the connection to the server keep in mind that the host should be the alias to the network e.g. `datamodelingpostgres-pgdatabase-1` or the IP of the container (This may change when the service is started), using the alias is recommended. If not sure which is the alias find the container ID and then get the aliases with the container ID.

```bash
docker ps -a
```

Remember to select the ID that corresponds to the Postgres Image, not PgAdmin.

```bash
docker inspect {CONTAINER_ID}  | grep -A 4 Aliases
```