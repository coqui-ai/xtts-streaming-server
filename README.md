# XTTS streaming server

1. Build the Docker container:

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

3. Generate audio with the test script:

```bash
$ cd test
$ python test_streaming.py
```
