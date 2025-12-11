# Stage 1: Build environment
FROM --platform=linux/arm64/v8 python:3.12-slim AS builder
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install pipenv
RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get install -y build-essential libcairo2-dev libpango1.0-dev libgdk-pixbuf-xlib-2.0-dev libffi-dev libxml2 libxslt1.1 && \
    apt-get install -y weasyprint python3-cairocffi && \
    apt-get install -y sqlite3 && \
    pip install pipenv

# Copy the Pipfiles only to cache dependencies
COPY Pipfile Pipfile.lock ./

COPY db/* ./

# Install dependencies in the system python environment
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system

# Copy the rest of your application code
COPY .. .

# Expose the port the app runs on
EXPOSE 5000
EXPOSE 5678

# Command to run the application
#CMD ["python", "-Xfrozen_modules=off", "launch.py", "runserver", "--host", "0.0.0.0", "--port", "5000"]
CMD ["python", "-Xfrozen_modules=off", "-m", "debugpy", "--listen", "0.0.0.0:5678", "launch.py", "runserver", "--host", "0.0.0.0", "--port", "5000"]
