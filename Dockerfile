FROM python:slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
# Create a volume mount point for data
VOLUME /app/data
CMD ["python", "app.py"]