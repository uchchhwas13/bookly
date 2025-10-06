FROM python:3.13.7

# Set working directory inside container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy project source code
COPY ./src /app/src
COPY ./migrations /app/migrations
COPY alembic.ini /app/alembic.ini


# Run the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]



