import gradio as gr
import requests

def clone_speaker(audio, speaker_name, state_vars):
    embeddings = requests.post(
        "http://localhost:8000/clone_speaker",
        json={"wav_file": audio}
    ).json()
    state_vars[speaker_name] = embeddings
    return state_vars

def tts(text, speaker_name, state_vars):
    embeddings = state_vars[speaker_name]
    generated_audio = requests.post(
        "http://localhost:8000/tts",
        json={
            "text": text,
            "language": "en",
            "speaker_embedding": embeddings["speaker_embedding"],
            "gpt_cond_latent": embeddings["gpt_cond_latent"]
        }
    ).content
    return generated_audio




