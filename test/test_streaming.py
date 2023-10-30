import argparse
import json
import shutil
import subprocess
import sys
import time
from typing import Iterator

import requests


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
        ffplay_cmd = ["ffplay", "-nodisp", "-probesize", "1024", "-autoexit", "-"]
    else:
        print("Saving to ", output_file)
        ffplay_cmd = ["ffmpeg", "-probesize", "1024", "-i", "-", output_file]

    ffplay_proc = subprocess.Popen(ffplay_cmd, stdin=subprocess.PIPE)
    for chunk in audio_stream:
        if chunk is not None:
            ffplay_proc.stdin.write(chunk)

    # close on finish
    ffplay_proc.stdin.close()
    ffplay_proc.wait()


def tts(text, speaker,language, server_url , decoder, stream_chunk_size) -> Iterator[bytes]:
    start = time.perf_counter()
    speaker["text"] = text
    speaker["language"] = language
    speaker["decoder"] = decoder  # "hifigan" or "ne_hifigan" for TTS>0.19.0
    speaker["stream_chunk_size"] = stream_chunk_size  # you can reduce it to get faster response, but degrade quality
    res = requests.post(
        f"{server_url}/tts_stream",
        json=speaker,
        stream=True,
    )
    end = time.perf_counter()
    print(f"Time to make POST: {end-start}s", file=sys.stderr)

    if res.status_code != 200:
        print("Error:", res.text)
        sys.exit(1)

    first = True
    for chunk in res.iter_content(chunk_size=512):
        if first:
            end = time.perf_counter()
            print(f"Time to first chunk: {end-start}s", file=sys.stderr)
            first = False
        if chunk:
            yield chunk

    print("⏱️ response.elapsed:", res.elapsed)


def get_speaker(ref_audio,server_url):
    files = {"wav_file": ("reference.wav", open(ref_audio, "rb"))}
    response = requests.post(f"{server_url}/clone_speaker", files=files)
    return response.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--text",
        default="It took me quite a long time to develop a voice and now that I have it I am not going to be silent.",
        help="text input for TTS"
    )
    parser.add_argument(
        "--language",
        default="en",
        help="Language to use default is 'en'  (English)"
    )

    parser.add_argument(
        "--output_file",
        default=None,
        help="Save TTS output to given filename"
    )
    parser.add_argument(
        "--ref_file",
        default=None,
        help="Reference audio file to use, when not given will use default"
    )
    parser.add_argument(
        "--server_url",
        default="http://localhost:8000",
        help="Server url http://localhost:8000 default, change to your server location "
    )
    parser.add_argument(
        "--decoder",
        default="ne_hifigan",
        help="Decoder for vocoder, ne_hifigan default, options ne_hifigan or hifigan"
    )

    parser.add_argument(
        "--stream_chunk_size",
        default="20",
        help="Stream chunk size , 20 default, reducing will get faster latency but may degrade quality"
    )

    args = parser.parse_args()

    with open("./default_speaker.json", "r") as file:
        speaker = json.load(file)

    if args.ref_file is not None:
        print("Computing the latents for a new reference...")
        speaker = get_speaker(args.ref_file,args.server_url)

    audio = stream_ffplay(tts(args.text, speaker,args.language,args.server_url,args.decoder,args.stream_chunk_size), args.output_file, save=bool(args.output_file))
