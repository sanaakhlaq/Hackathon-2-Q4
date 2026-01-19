FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything to the container
COPY . .

# Check if the code is in a backend folder and adjust accordingly
# If your main.py is in the backend folder, uncomment the next line:
# WORKDIR /app/backend

EXPOSE 7860

# Adjust the path if your main.py is in the backend folder:
# If main.py is in the backend folder, use: CMD ["python", "backend/main.py"]
# Otherwise, use the default: CMD ["python", "main.py"]
CMD ["python", "main.py"]