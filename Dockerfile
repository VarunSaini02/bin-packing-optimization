FROM python:3.8-alpine as alex
COPY src/alex.py .
RUN pip install flask
CMD ["python", "alex.py"]

FROM python:3.8-alpine as carla
COPY src/carla.py .
RUN pip install flask
CMD ["python", "carla.py"]

# FROM python:3.8-alpine as test
# COPY src/test.py .
# RUN pip install flask
# CMD ["python", "test.py"]