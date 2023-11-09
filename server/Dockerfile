FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

RUN apt-get update && \
    apt-get install --no-install-recommends -y sox libsox-fmt-all curl wget gcc git git-lfs build-essential libaio-dev libsndfile1 ssh ffmpeg && \
    apt-get clean && apt-get -y autoremove

WORKDIR /app
COPY requirements.frozen.txt .
RUN python -m pip install --no-deps -r requirements.frozen.txt \
    && python -m pip cache purge

COPY main.py .

ENV NUM_THREADS=2
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
