# Slim version of python for small image
FROM python:3.10-slim
# working directory in the container
WORKDIR /app

#Copy and install the dependencies first (better for caching)
COPY requirements.txt .
RUN pip install -r requirements.txt

#Copy the rest of the code 
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]