import gradio as gr
import requests
import base64
import tempfile
import os

SERVER_URL = 'http://localhost:8000'
try:
    STUDIO_SPEAKERS = requests.get(SERVER_URL + "/studio_speakers").json()
except:
    raise Exception("Please make sure the server is running first.")

cloned_speakers = {}

def clone_speaker(upload_file, clone_speaker_name, cloned_speaker_names):
    files = {"wav_file": ("reference.wav", open(upload_file, "rb"))}
    embeddings = requests.post(
        SERVER_URL + "/clone_speaker",
        files=files,
    ).json()
    cloned_speakers[clone_speaker_name] = embeddings
    cloned_speaker_names.append(clone_speaker_name)
    return cloned_speaker_names, gr.Dropdown.update(choices=cloned_speaker_names)

def tts(text, speaker_type, speaker_name_studio, speaker_name_custom):
    embeddings = STUDIO_SPEAKERS[speaker_name_studio] if speaker_type == 'Studio' else cloned_speakers[speaker_name_custom]
    generated_audio = requests.post(
        SERVER_URL + "/tts",
        json={
            "text": text,
            "language": "en",
            "speaker_embedding": embeddings["speaker_embedding"],
            "gpt_cond_latent": embeddings["gpt_cond_latent"]
        }
    ).content
    generated_audio = base64.b64decode(generated_audio)
    if not os.path.exists("demo_outputs"):
        os.mkdir("demo_outputs")
    generated_audio_path = os.path.join("demo_outputs", next(tempfile._get_candidate_names()) + ".wav")
    with open(generated_audio_path, "wb") as fp:
        fp.write(generated_audio)
        generated_audio = fp.name
    return generated_audio

with gr.Blocks() as demo:
    cloned_speaker_names = gr.State([])
    with gr.Tab("TTS"):
        with gr.Row() as col4:
            speaker_name_studio = gr.Dropdown(label="Studio speaker", choices=STUDIO_SPEAKERS.keys())
            speaker_name_custom = gr.Dropdown(label="Cloned speaker", choices=cloned_speaker_names.value)
        with gr.Column() as col2:
            speaker_type = gr.Dropdown(label="Speaker type", choices=["Studio", "Cloned"], value="Studio")
            text = gr.Textbox(label="text")
            tts_button = gr.Button(value="TTS")
        with gr.Column() as col3:
            generated_audio = gr.Audio(label="Generated audio", autoplay=True)
    with gr.Tab("Clone a new speaker"):
        with gr.Column() as col1:
            upload_file = gr.Audio(label="Upload reference audio", type="filepath")
            clone_speaker_name = gr.Textbox(label="Speaker name", value="default_speaker")
            clone_button = gr.Button(value="Clone speaker")

    clone_button.click(
        fn=clone_speaker,
        inputs=[upload_file, clone_speaker_name, cloned_speaker_names],
        outputs=[cloned_speaker_names, speaker_name_custom],
    )

    tts_button.click(
        fn=tts,
        inputs=[text, speaker_type, speaker_name_studio, speaker_name_custom],
        outputs=[generated_audio],
    )

if __name__ == "__main__":
    demo.launch(
        share=True,
        debug=True,
        server_port=3009,
        server_name="0.0.0.0",
    )
