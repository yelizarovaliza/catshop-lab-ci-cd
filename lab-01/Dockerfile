# 1. Use Python 3.12
FROM python:3.12-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy dependencies list
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install -r requirements.txt

# 5. Copy application files
COPY . .

# 6. Document the port used by the application
EXPOSE 8080

# 7. Start the application
CMD ["python", "app.py"]