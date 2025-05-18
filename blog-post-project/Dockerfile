FROM python:3.12.3-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project into container
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Run Flask app
ENV FLASK_APP=main.py
#Enable auto-reload
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]