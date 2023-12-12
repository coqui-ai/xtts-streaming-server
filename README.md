# XTTS streaming server

## Running the server

To run a pre-built container (CUDA 11.8):

```bash
$ docker run --gpus=all -e COQUI_TOS_AGREED=1 --rm -p 8000:80 ghcr.io/coqui-ai/xtts-streaming-server:latest
```

CUDA 12.1 version (for newer cards) 
```bash
$ docker run --gpus=all -e COQUI_TOS_AGREED=1 --rm -p 8000:80  ghcr.io/coqui-ai/xtts-streaming-server:latest-cuda121
```

Run with a custom XTTS v2 model (FT or previous versions):
```bash
$ docker run -v /path/to/model/folder:/app/tts_models --gpus=all -e COQUI_TOS_AGREED=1  --rm -p 8000:80 ghcr.io/coqui-ai/xtts-streaming-server:latest`
```

Setting the `COQUI_TOS_AGREED` environment variable to `1` indicates you have read and agreed to
the terms of the [CPML license](https://coqui.ai/cpml).

(Fine-tuned XTTS models also are under the [CPML license](https://coqui.ai/cpml))

## Testing the server

### Using the gradio demo

```bash
$ python -m pip install -r test/requirements.txt
$ python demo.py
```

### Using the test script

```bash
$ cd test
$ python -m pip install -r requirements.txt
$ python test_streaming.py
```

## Building the container

1. To build the Docker container Pytorch 2.1 and CUDA 11.8 :

```bash
$ cd server
$ docker build -t xtts-stream .
```
For Pytorch 2.1 and CUDA 12.1 :
```bash
$ cd server
docker build -t xtts-stream . -f Dockerfile.cuda121
```
2. Run the server container:

```bash
$ docker run --gpus all -e COQUI_TOS_AGREED=1 --rm -p 8000:80 xtts-stream
```

Setting the `COQUI_TOS_AGREED` environment variable to `1` indicates you have read and agreed to
the terms of the [CPML license](https://coqui.ai/cpml).


Make sure the model folder contains the following files:
- `config.json`
- `model.pth`
- `vocab.json`

