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

If you have already downloaded v1.1 model and like to use this server, and using Ubuntu, change your /home/YOUR_USER_NAME
```bash
$ docker run -v /home/YOUR_USER_NAME/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v1.1:/root/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v1.1 --env NVIDIA_DISABLE_REQUIRE=1 --gpus=all -e COQUI_TOS_AGREED=1  --rm -p 8000:80 ghcr.io/coqui-ai/xtts-streaming-server:latest-cuda118`
```
Setting the `COQUI_TOS_AGREED` environment variable to `1` indicates you have read and agreed to
the terms of the [CPML license](https://coqui.ai/cpml).

## Testing the server

1. Generate audio with the test script:

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
$ docker run --gpus=all -e COQUI_TOS_AGREED=1 --rm -p 8000:80 xtts-stream
```

Setting the `COQUI_TOS_AGREED` environment variable to `1` indicates you have read and agreed to
the terms of the [CPML license](https://coqui.ai/cpml).
