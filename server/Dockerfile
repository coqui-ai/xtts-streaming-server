FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-devel
WORKDIR /app
COPY requirements.txt .


COPY pipconfig.conf .
ARG PIP_CONFIG_FILE=pipconfig.conf
RUN python -m pip install -r requirements.txt

COPY main.py .

# This is for not complaining 11.8 on 11.7 driver
# It is compatible
ARG NVIDIA_DISABLE_REQUIRE=1

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
