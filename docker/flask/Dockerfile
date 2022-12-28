FROM python:3.9-slim-bullseye

# Mount src directory to /app
ADD ./src /app
WORKDIR /app

# Expose Port
EXPOSE 5000

# Install dependencies
RUN pip install -r requirements.txt
CMD ["python3", "-m", "flask", "--debug", "run", "--host=0.0.0.0"]
