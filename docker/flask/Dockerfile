FROM python:3.9-slim-bullseye

# Mount src directory to /app
ADD ./src /app
WORKDIR /app

# Expose Port
EXPOSE 5000

# Install dependencies
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "build-essential", "python3-dev", "uwsgi"]
RUN ["python3", "-m", "pip", "install", "-r", "requirements.txt"]
CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol=http", "-w", "wsgi:app", "--master"] 
