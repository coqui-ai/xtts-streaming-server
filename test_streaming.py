import argparse
import shutil
import subprocess
import sys
import time
import json
import requests
import copy
import os
from io import BytesIO
from typing import Iterator

def is_installed(lib_name: str) -> bool:
    lib = shutil.which(lib_name)
    if lib is None:
        return False
    return True

def save(audio: bytes, filename: str) -> None:
    with open(filename, "wb") as f:
        f.write(audio)

def stream_ffplay(audio_stream, output_file, save=True):
    if not save:
        ffplay_cmd = ["ffplay", "-autoexit", "-"]
    else:
        print("Saving to ", output_file)
        ffplay_cmd = ["ffmpeg", "-i", "-", output_file]

    ffplay_proc = subprocess.Popen(ffplay_cmd, stdin=subprocess.PIPE)
    for chunk in audio_stream:
        if chunk is not None:
            ffplay_proc.stdin.write(chunk)

    # close on finish
    ffplay_proc.stdin.close()
    ffplay_proc.wait()

def tts(text, speaker) -> Iterator[bytes]:
    start = time.perf_counter()
    speaker["text"] = text
    speaker["language"] = "en"
    res = requests.post(
        "http://localhost:5000/predict_streaming/",
        json=speaker,
        stream=True,
    )
    end = time.perf_counter()
    print(f"Time to make POST: {end-start}s", file=sys.stderr)
    first = True
    for chunk in res.iter_content(chunk_size=None):
        if first:
            end = time.perf_counter()
            print(f"Time to first chunk: {end-start}s", file=sys.stderr)
            first = False
        if chunk:
            print("chunk len:", len(chunk))
            yield chunk

    print("⏱️ response.elapsed:", res.elapsed)

def get_speaker(ref_audio):
    files = {"wav_file": ("reference.wav", open(ref_audio, "rb"))}
    response = requests.post(f"http://localhost:5000/predict_speaker", files=files)
    return response.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--text",
        default="It took me quite a long time to develop a voice and now that I have it I am not going to be silent.",
    )
    parser.add_argument(
        "--output_file",
        default="./output.mp3",
    )
    parser.add_argument(
        "--ref_file",
        default=None,
    )
    args = parser.parse_args()

    with open('./default_speaker.json', 'r') as file:
        speaker = json.load(file)
    
    if args.ref_file is not None:
        print("Computing the latents for a new reference...")
        speaker = get_speaker(args.ref_file)

    audio = stream_ffplay(tts(args.text, speaker), args.output_file, save=True)