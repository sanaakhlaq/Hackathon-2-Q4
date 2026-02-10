FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything to the container
COPY . .

EXPOSE 7860

# Run the FastAPI application
CMD ["python", "main.py"]