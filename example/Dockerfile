FROM python:3.9-slim
WORKDIR /app

# Copy required files

COPY example.py /app/

COPY requirements.txt /app/

COPY entrypoint.py /app/

COPY report_engine.py /app/


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint
ENTRYPOINT ["python", "entrypoint.py"]