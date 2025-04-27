import subprocess

# Paths to CLI tools
LLAMA_CLI = "/home/piumalnipun9/llama.cpp/build/bin/llama-cli"
WHISPER_CLI = "/home/piumalnipun9/whisper.cpp/build/bin/whisper-cli"

# Model paths
LLAMA_MODEL = "/home/piumalnipun9/llama.cpp/model.gguf"
WHISPER_MODEL = "/home/piumalnipun9/whisper.cpp/models/ggml-tiny.en.bin"

# Function to transcribe audio using whisper.cpp
def transcribe_audio(audio_file):
    whisper_cmd = [
        WHISPER_CLI, "-m", WHISPER_MODEL, "-f", audio_file
    ]

    print("Transcribing audio...")
    result = subprocess.run(whisper_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Whisper error:", result.stderr)
        return None

    raw_output = result.stdout.strip()

    # Clean output: extract only spoken lines
    lines = raw_output.splitlines()
    speech_lines = []
    for line in lines:
        if "]" in line:
            try:
                speech = line.split("]")[1].strip()
                if speech:
                    speech_lines.append(speech)
            except IndexError:
                continue

    cleaned_text = "\n".join(speech_lines)
    return cleaned_text

# Function to chat with llama.cpp
def chat_with_llama(prompt):
    llama_cmd = [
        LLAMA_CLI,
        "-m", LLAMA_MODEL,
        "-p", prompt,
    ]

    print("Generating response from LLaMA...")
    result = subprocess.run(llama_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("LLaMA error:", result.stderr)
        return None

    return result.stdout.strip()

# Main execution
if __name__ == "__main__":
    audio_file = "/home/piumalnipun9/whisper.cpp/samples/jfk.wav"  # Change to your audio file if needed

    # Step 1: Transcribe
    transcription = transcribe_audio(audio_file)
    if not transcription:
        print("Transcription failed.")
        exit(1)

    print("\n Transcription:\n")
    print(transcription)

    # Step 2: Chat with LLaMA
    response = chat_with_llama(transcription)
    if not response:
        print("LLaMA response failed.")
        exit(1)

    print("\n LLaMA Response:\n")
    print(response)
