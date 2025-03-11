# Streaming Data Pipeline

**Overview**
A real-time data pipeline using:
>Kafka for message streaming

>Python for data processing

>TimescaleDB (PostgreSQL-based) for time-series storage

>Grafana for real-time data visualization

**Architecture**
Data Generator (Python) → Produces color and value data to Kafka.
Kafka → Handles message streaming.
Python Worker → Consumes messages, aggregates, and stores them in TimescaleDB.
TimescaleDB → Stores aggregated time-series data.
Grafana → Connects to TimescaleDB for visualization.

**1. Prerequisites:**
  Docker & Docker Compose
  Python (Run the following commands to import python packages: pip install kafka-python, pip install psycopg2-binary )
**2. Setup and Run:**
    *Kafka:*
      To run both kafka and zookeeper in docker container:
        To run Docker Compose file zk-single-kafka-single.yml in the folder dockerKafka (Reference : https://github.com/conduktor/kafka-stack-docker-compose/blob/master/zk-single-kafka-single.yml) Comand line:
        ```
        docker compose -f zk-single-kafka-single.yml up -d
        ```
        Zookeeper will be available at `$DOCKER_HOST_IP:2181`
        Kafka will be available at `$DOCKER_HOST_IP:9092`
      To create topic:
        ```
        docker exec kafka1 kafka-topics --bootstrap-server kafka:9092 --create --topic workerData1
        ```
    *Phthon files:*
      To run `data_generator.py`:
        From the dockerDataGenerator Folder, run the following commands,
        ```
        docker build -t pythondatagenerator .
        docker run pythondatagenerator
        ```
      To run `workers.py`:
        From the dockerWorker folder, run the following commands,
        ```
        docker build -t pythonworker .
        docker run pythonworker
        ```
    *TimescaleDB (Time series database):* 
        Timescale BD is a cloud instance,
        The credentials of the db :
                        > host=t4h6sqbzyc.xq0dr8321m.tsdb.cloud.timescale.com
                        > port=35046
                        > user=tsdbadmin
                        > password=rs0b9u57afc1f344
                        > dbname=tsdb
                        > table=message (to save sum, average, timestamp of color values collected in the interval)
                        > table=aggregate (to save aggrigate average, count of colors when new values are stored)
      *Grafana:*
        Grafana is installed through docker command:
        ```
        docker run -d -p 3000:3000 --name=grafana --volume grafana-storage:/var/lib/grafana grafana/grafana-enterprise
        ```
        It can be accessed from `localhost:3000`, ensures that Grafana’s data is persisted across container restarts.
        Alert, Data source and Dashboard configurations (screenshots):
        > Data Source configuration:
         ![image](https://github.com/user-attachments/assets/aa9f8c88-6c6a-4f09-91ce-4ad986124dad)
        > SMTP configuration:
        ![Screenshot 2025-03-11 180915](https://github.com/user-attachments/assets/396d3842-e545-4f55-b773-d53e1b2b42b9)
        > Alert Configuration (If Average values of any color exceeds 75 at the interval will trigger mail)
        ![image](https://github.com/user-attachments/assets/675c90a1-4d29-4e09-8f32-3bbd48e4318c)
        > Triggered mail:
        ![image](https://github.com/user-attachments/assets/6df7f161-1e92-4dd8-a9c6-34af684c041f)
        >Dashboard -> Time vs Average configuration:
        ![Screenshot 2025-03-11 180342](https://github.com/user-attachments/assets/46179489-f44e-472b-ab93-9da42c1d755b)
        ![Screenshot 2025-03-11 180328](https://github.com/user-attachments/assets/bf086efa-5449-4c47-88a8-1ffce27e6c96)
        > Dashboard -> Running Average configuration:
        ![image](https://github.com/user-attachments/assets/646c5036-acf8-43d9-9979-c3ce2e513a60)
        ![image](https://github.com/user-attachments/assets/ebd1eb92-ef0c-4e2b-8523-fcaed1b49db6)
        In Each queries only the color filter is changed for respective colors.

        Dashboard preview:
        ![image](https://github.com/user-attachments/assets/0be3fd3e-80b7-4c40-85a5-26c4a7f1ccfb)
        
Final Docker containers setup:
![Screenshot 2025-03-11 150006](https://github.com/user-attachments/assets/28d8d149-4913-4e0b-b24a-0d379ff91ff4)
