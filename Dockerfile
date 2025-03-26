# Use official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy all files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose FastAPI on port 8000 and Streamlit on port 8501
EXPOSE 8000
EXPOSE 8501

# Run both FastAPI and Streamlit
CMD uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0


