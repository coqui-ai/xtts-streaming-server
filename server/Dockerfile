FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-devel
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends -y sox libsox-fmt-all curl wget gcc git git-lfs build-essential libaio-dev libsndfile1 ssh ffmpeg && \
    apt-get clean && apt-get -y autoremove

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --use-deprecated=legacy-resolver -r requirements.txt \
    && python -m pip cache purge

RUN python -m unidic download

COPY main.py .
ENV NVIDIA_DISABLE_REQUIRE=1

ENV NUM_THREADS=2
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
