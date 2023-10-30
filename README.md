# XTTS streaming server

## Running the server

To run a pre-built container:

```bash
$ docker run --gpus=all -e COQUI_TOS_AGREED=1 --rm -p 8000:80 ghcr.io/coqui-ai/xtts-streaming-server:latest
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

1. To build the Docker container:

```bash
$ cd server
$ docker build -t xtts-stream .
```
2. Run the server container:

```bash
$ docker run --gpus=all -e COQUI_TOS_AGREED=1 --rm -p 8000:80 xtts-stream
```

Setting the `COQUI_TOS_AGREED` environment variable to `1` indicates you have read and agreed to
the terms of the [CPML license](https://coqui.ai/cpml).
