# XTTS streaming server


https://github.com/coqui-ai/xtts-streaming-server/assets/17219561/7220442a-e88a-4288-8a73-608c4b39d06c


## 1) Run the server

### Use a pre-built image

CUDA 12.1:

```bash
$ docker run --gpus=all -e COQUI_TOS_AGREED=1 --rm -p 8000:80 ghcr.io/coqui-ai/xtts-streaming-server:latest-cuda121
```

CUDA 11.8 (for older cards):

```bash
$ docker run --gpus=all -e COQUI_TOS_AGREED=1 --rm -p 8000:80 ghcr.io/coqui-ai/xtts-streaming-server:latest
```

CPU (not recommended):

```bash
$ docker run -e COQUI_TOS_AGREED=1 --rm -p 8000:80 ghcr.io/coqui-ai/xtts-streaming-server:latest-cpu
```

Run with a fine-tuned model:

Make sure the model folder `/path/to/model/folder`  contains the following files:
- `config.json`
- `model.pth`
- `vocab.json`

```bash
$ docker run -v /path/to/model/folder:/app/tts_models --gpus=all -e COQUI_TOS_AGREED=1  --rm -p 8000:80 ghcr.io/coqui-ai/xtts-streaming-server:latest`
```

Setting the `COQUI_TOS_AGREED` environment variable to `1` indicates you have read and agreed to
the terms of the [CPML license](https://coqui.ai/cpml). (Fine-tuned XTTS models also are under the [CPML license](https://coqui.ai/cpml))

### Build the image yourself

To build the Docker container Pytorch 2.1 and CUDA 11.8 :

`DOCKERFILE` may be `Dockerfile`, `Dockerfile.cpu`, `Dockerfile.cuda121`, or your own custom Dockerfile.

```bash
$ git clone git@github.com:coqui-ai/xtts-streaming-server.git
$ cd xtts-streaming-server/server
$ docker build -t xtts-stream . -f DOCKERFILE
$ docker run --gpus all -e COQUI_TOS_AGREED=1 --rm -p 8000:80 xtts-stream
```

Setting the `COQUI_TOS_AGREED` environment variable to `1` indicates you have read and agreed to
the terms of the [CPML license](https://coqui.ai/cpml). (Fine-tuned XTTS models also are under the [CPML license](https://coqui.ai/cpml))

## 2) Testing the running server

Once your Docker container is running, you can test that it's working properly. You will need to run the following code from a fresh terminal.

### Clone `xtts-streaming-server` if you haven't already

```bash
$ git clone git@github.com:coqui-ai/xtts-streaming-server.git
```

### Using the gradio demo

```bash
$ cd xtts-streaming-server
$ python -m pip install -r test/requirements.txt
$ python demo.py
```

### Using the test script

```bash
$ cd xtts-streaming-server/test
$ python -m pip install -r requirements.txt
$ python test_streaming.py
```
