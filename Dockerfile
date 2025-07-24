FROM python:3.11-slim-buster
WORKDIR /mlh-pe-portfolio-site
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host=0.0.0.0"]
EXPOSE 5000