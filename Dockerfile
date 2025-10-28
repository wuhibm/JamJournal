#Stage 1: Build the base
FROM python:3.13-slim AS builder

#Create app directory
RUN mkdir /app

#Set working directory
WORKDIR /app

#Set environment variables for python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

#Install dependencies    
RUN pip install --upgrade pip
COPY requirements.txt /app/ 
RUN pip install --no-cache-dir -r requirements.txt

#Stage 2: Create the final image
FROM python:3.13-slim

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

#Copy python dependencies from builder stage    
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY --chown=appuser:appuser /capstone .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

#Change to a non-root user
USER appuser

#Expose port 8000
EXPOSE 8000

# Make entrypoint script executable by modifying its permissions
# RUN chmod +x /app/entrypoint.prod.sh
RUN python manage.py collectstatic --noinput

#Run the entrypoint script
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "capstone.wsgi:application"]