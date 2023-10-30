FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-devel
WORKDIR /app
COPY requirements.txt .

ARG PIP_CONFIG_FILE=pipconfig.conf
RUN python -m pip install -r requirements.txt

COPY main.py .

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
