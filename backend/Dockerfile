FROM python:3.10-slim

# Prevent Python from buffering stdout/err
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install python deps first for better layer-caching
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source **after** deps (relative to the Dockerfile)
COPY backend/ /code/
# Always run migrations, then start Gunicorn
CMD ["sh", "-c", "alembic upgrade head && gunicorn -c gunicorn_conf.py app.main:app"]