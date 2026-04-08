FROM python:3.10-slim

WORKDIR /app

# Install project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Run inference script and then keep container alive to satisfy Hugging Face Spaces requirements
CMD python inference.py && tail -f /dev/null
