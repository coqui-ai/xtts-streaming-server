FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY main.py .

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
