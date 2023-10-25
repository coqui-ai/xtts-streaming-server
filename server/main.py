import io, os, time, sys, signal
import json, yaml
import base64

from fastapi import (
    FastAPI,
    File,
    Body,
    UploadFile,
    Request,
    Response,
    status,
)
from fastapi.responses import StreamingResponse

import tempfile
import asyncio
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.status import HTTP_504_GATEWAY_TIMEOUT
from anyio.lowlevel import RunVar
from anyio import CapacityLimiter
from exceptiongroup import ExceptionGroup, BaseExceptionGroup
from exceptiongroup import catch as catch_exception_group

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.utils.manage import ModelManager
from TTS.utils.generic_utils import get_user_data_dir

import numpy as np
import torchaudio
import torch
import time
import wave

torch.set_num_threads(8)
device = torch.device("cuda")

model_name = "tts_models/multilingual/multi-dataset/xtts_v1.1"
ModelManager().download_model(model_name)
model_path = os.path.join(get_user_data_dir("tts"), model_name.replace("/", "--"))

config = XttsConfig()
config.load_json(os.path.join(model_path, "config.json"))
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir=model_path, eval=True, use_deepspeed=False)
model.to(device)

##### Run fastapi #####
app = FastAPI(
    title="XTTS Multilang streaming Fastapi",
    description="""XTTS Multilang streaming Fastapi""",
    version="0.0.1",
    docs_url="/",
)

##################### MIDDLEWARE ######################################

@app.on_event("startup")
async def startup():
    print("Fastapi startup...")
    thread_limit = int(os.getenv("THREAD_LIMIT", 8))
    RunVar("_default_thread_limiter").set(CapacityLimiter(8))


def limit_one_at_a_time(f):
    async def wrapper(*args, **kwargs):
        async with limit_semaphore:
            return await f(*args, **kwargs)
    return wrapper

# For streaming we put semaphore inside the stream_handler
async def stream_handler(gen):
    async with limit_semaphore:
        # Will wrap into streamer to catch cancel events
        try:
            for i in gen:
                yield i
                # To enable request canceling we need a little timeout here or it just processes on cancel
                #await asyncio.sleep(0.005)
            # Clear cache or VRAM usage keeps growing
            torch.cuda.empty_cache()
        except asyncio.CancelledError:
            print("Request cancelled.")
            # Clear cache or VRAM usage keeps growing
            torch.cuda.empty_cache()

@limit_one_at_a_time
@app.post("/predict_speaker")
async def predict_speaker(wav_file: UploadFile):
    """Compute conditioning inputs from reference audio file."""
    temp_audio_name = next(tempfile._get_candidate_names())
    with open(temp_audio_name, "wb") as temp, torch.inference_mode():
        temp.write(io.BytesIO(wav_file.file.read()).getbuffer())
        gpt_cond_latent, _, speaker_embedding = model.get_conditioning_latents(temp_audio_name)
    return {
        "gpt_cond_latent": gpt_cond_latent.cpu().squeeze().half().tolist(),
        "speaker_embedding": speaker_embedding.cpu().squeeze().half().tolist(),
    }

##############################
### GPT STREAMING
##############################

def postprocess(wav):
    """Post process the output waveform"""
    if isinstance(wav, list):
        wav = torch.cat(wav, dim=0)
    wav = wav.clone().detach().cpu().numpy()
    wav = wav[None, : int(wav.shape[0])]
    wav = np.clip(wav, -1, 1)
    wav = (wav * 32767).astype(np.int16)
    return wav

def encode_audio_common(
    frame_input, encode_base64=True, sample_rate=24000, sample_width=2, channels=1
):
    """Return base64 encoded audio"""
    wav_buf = io.BytesIO()
    with wave.open(wav_buf, "wb") as vfout:
        vfout.setnchannels(channels)
        vfout.setsampwidth(sample_width)
        vfout.setframerate(sample_rate)
        vfout.writeframes(frame_input)

    wav_buf.seek(0)
    if encode_base64:
        b64_encoded = base64.b64encode(wav_buf.getbuffer()).decode("utf-8")
        return b64_encoded
    else:
        return wav_buf.read()

async def predict_streaming(parsed_input: dict = Body(...)):
    speaker_embedding = torch.tensor(parsed_input["speaker_embedding"]).unsqueeze(0).unsqueeze(-1)
    gpt_cond_latent = torch.tensor(parsed_input["gpt_cond_latent"]).reshape((-1,1024)).unsqueeze(0)
    text = parsed_input["text"]
    language = parsed_input["language"]

    sample_width = int(parsed_input.get("sample_width", 2))
    add_wav_header = int(parsed_input.get("add_wav_header", 1))

    chunks = model.inference_stream(text, language, gpt_cond_latent, speaker_embedding)
    for i, chunk in enumerate(chunks):
        chunk = postprocess(chunk)
        if i == 0 and add_wav_header :
            yield encode_audio_common(
                b"", encode_base64=False, sample_width=sample_width
            )
            yield chunk.tobytes()
        else:
            yield chunk.tobytes()

@app.post("/predict_streaming")
def predict_streaming_endpoint(parsed_input: dict = Body(...)):
    return StreamingResponse(
        predict_streaming(parsed_input),
        media_type="audio/wav",
    )