FROM python
WORKDIR /app
COPY . /app
RUN pip install kafka-python
CMD ["python3","data_generator.py"]
