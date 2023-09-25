FROM python:3.8-alpine as alex
COPY src/alex.py .
RUN pip install flask
CMD ["python", "alex.py"]

FROM python:3.8-alpine as carla
COPY src/carla.py .
RUN pip install flask
CMD ["python", "carla.py"]

FROM python:3.8-alpine as algo-eval
COPY src/algo-eval.py .
RUN pip install flask requests
CMD ["python", "algo-eval.py"]

FROM python:3.8-alpine as algo-eval-storage
COPY src/algo-eval-storage.py .
RUN pip install flask
CMD ["python", "algo-eval-storage.py"]