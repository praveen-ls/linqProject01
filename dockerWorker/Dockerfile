FROM python
WORKDIR /appWorker
COPY . /appWorker
RUN pip install kafka-python
RUN pip install psycopg2-binary 
CMD ["python3","worker.py"]