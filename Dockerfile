FROM python:3.8
WORKDIR /usr/src/app
COPY . .
RUN pip install poetry
RUN poetry install
RUN poetry shell
EXPOSE 5000
CMD ["python", "app.py"]
