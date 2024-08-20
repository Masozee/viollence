FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install granian

# Copy project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run granian
CMD ["granian", "--interface", "wsgi", "--host", "0.0.0.0", "--port", "7000", "core.wsgi:application"]