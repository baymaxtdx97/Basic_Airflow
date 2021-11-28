# Creating Airflow DAG - Transferring data from different databases
This project aims to create a simple DAG to transfer data from different databases. 


# Project Structure 

```
├── dags
│   ├── sql
│   │   ├── create_table.sql
│   │   └── insert_values.sql
│   └── dag_data_transfer.py
├── docker-compose.yaml
├── logs
└── plugins

```


# Getting started 
For this project, a basic airflow configuration is taken from the source. To get the docker compose file for this version, you can run

```bash
 curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.0.0/docker-compose.yaml'
```

# Postgres Database
In this project, two different databases are created using docker. The two images are created in docker-compose.yaml. The two images are created using the following configurations

```
db1_source_database:
    image: postgres:13
    restart: always
    ports:
      - 5431:5432
    environment:
      POSTGRES_DB: project_x
      POSTGRES_USER: user123
      POSTGRES_PASSWORD: 123456
    volumes:
      - db-data:/var/lib/postgresql/data
```

```
db2_source_database:
    image: postgres:13
    restart: always
    ports:
      - 5430:5432
    environment:
      POSTGRES_DB: project_y
      POSTGRES_USER: user1234
      POSTGRES_PASSWORD: 123456
    volumes:
      - db2-data:/var/lib/postgresql/data
```

For this project, a table called new_table is created in both databases. The attributes of the table can be found in create_table.sql. No Constraints have been applied
to the tables as it is not the focus of this project.

# Airflow 

To run the dags, there is a need to create a connection in Airflow UI for the postgres databases. For each database, the configuration can be followed above. The name of the connection should follow the following names
- db1_source_database => postgres_default_project_x
- db2_source_database => postgres_default_project_y


# DAG
There are 2 nodes in this dag. The first node is to populate some values into the source table. The query can be found in insert_values.sql. The second node conducts the 
actual transferrence of data to the destination table. The destination table will take all the rows in the source table and be replicated over.




