FROM python:3.11.7
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends -y sox libsox-fmt-all curl wget gcc git git-lfs build-essential libaio-dev libsndfile1 ssh ffmpeg && \
    apt-get clean && apt-get -y autoremove

WORKDIR /app
COPY requirements_cpu.txt .
RUN python -m pip install --use-deprecated=legacy-resolver -r requirements_cpu.txt \
    && python -m pip cache purge

RUN python -m unidic download
RUN mkdir -p /app/tts_models

COPY main.py .
ENV USE_CPU=1

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
