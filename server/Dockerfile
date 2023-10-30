FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel
WORKDIR /app
COPY requirements.frozen.txt .
RUN python -m pip install --no-deps -r requirements.frozen.txt \
    && python -m pip cache purge

COPY main.py .

ENV NUM_THREADS=2
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
