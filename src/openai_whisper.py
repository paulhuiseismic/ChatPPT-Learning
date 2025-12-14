from transformers import pipeline
import gradio as gr
import torch
import tempfile
import os
import subprocess

from logger import LOG


# Get the absolute path to the model directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_NAME = os.path.join(SCRIPT_DIR, "..", "models", "whisper-large-v3")
MODEL_NAME = os.path.normpath(MODEL_NAME)  # Normalize the path for Windows
BATCH_SIZE = 8 # Number of samples to process in a batch

device = "cuda:0" if torch.cuda.is_available() else "cpu"

pipe = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    chunk_length_s=60,
    device=device
)

def convert_to_wav(input_path):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
        output_path = temp_wav_file.name

    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", output_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return output_path
    except subprocess.CalledProcessError as e:
        LOG.error(f"Error converting file to WAV: {e}")
        if os.path.exists(output_path):
            os.remove(output_path)
        raise gr.Error("Error converting file to WAV")
    except FileNotFoundError as e:
        LOG.error(f"Not found ffmpeg executable: {e}")
        if os.path.exists(output_path):
            os.remove(output_path)
        raise gr.Error("ffmpeg is not installed or not found in PATH")

def asr(audio_file, task="transcribe"):
    wav_file = convert_to_wav(audio_file)

    try:
        result = pipe(
            wav_file,
            batch_size=BATCH_SIZE,
            generate_kwargs={"task": task},
            return_timestamps=True
        )
        text = result["text"]
        LOG.info(f"[recognized result]: {text}")

        return text
    except Exception as e:
        LOG.error(f"Error during ASR processing: {e}")
        raise gr.Error("Error during ASR processing")
    finally:
        if os.path.exists(wav_file):
            os.remove(wav_file)

def transcribe(inputs, task):
    LOG.info(f"[transcribe] inputs: {inputs}")

    if not inputs or not os.path.exists(inputs):
        raise gr.Error("No input files found")

    file_ext = os.path.splitext(inputs)[1].lower()
    if file_ext not in ['.wav', '.flac', '.mp3']:
        LOG.error(f"Invalid file extension: {file_ext}")
        raise gr.Error("Invalid file extension")

    return asr(inputs, task)

mf_transcribe = gr.Interface(
    fn=transcribe,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Microphone"),
        gr.Radio(choices=["transcribe", "translate"], value="transcribe", label="Task Type"),
    ],
    outputs="text",
    title="Whisper Large V3: transcribe/translate from microphone",
    description="Upload an audio file or record from microphone to transcribe or translate using OpenAI Whisper Large V3 model.",
    flagging_mode="never"
)

file_transcribe = gr.Interface(
    fn=transcribe,
    inputs=[
        gr.Audio(sources=["upload"], type="filepath", label="Upload Audio File"),
        gr.Radio(choices=["transcribe", "translate"], value="transcribe", label="Task Type"),
    ],
    outputs="text",
    title="Whisper Large V3: transcribe/translate from audio file",
    description="Upload an audio file to transcribe or translate using OpenAI Whisper Large V3 model.",
    flagging_mode="never"
)

if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.TabbedInterface(
            [mf_transcribe, file_transcribe],
            ["Microphone Input", "File Upload"]
        )

    demo.queue().launch(
        share=False,
        server_name="0.0.0.0"
    )