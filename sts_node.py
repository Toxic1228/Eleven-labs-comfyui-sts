import requests
import os
import time
import tempfile
import torch
import torchaudio

class ElevenLabs_SpeechToSpeech:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO",), # Input is AUDIO
                "api_key": ("STRING", {"default": "YOUR_API_KEY_HERE"}),
                "voice_id": ("STRING", {"default": "JBFqnCBsd6RMkjVDRZzb"}),
            }
        }

    # --- THIS IS THE CHANGE ---
    RETURN_TYPES = ("STRING",) # Output is STRING
    RETURN_NAMES = ("output_audio_path",)
    # ------------------------
    
    FUNCTION = "run_speech_to_speech"
    CATEGORY = "My_Nodes"

    def run_speech_to_speech(self, audio, api_key, voice_id):
        
        # --- Error Checking ---
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            print("[ElevenLabs Node] Error: API Key is missing!")
            return ("Error: API Key is missing",)

        # --- Get Input Audio (with all fixes) ---
        try:
            if "samples" in audio:
                samples = audio["samples"]
            elif "waveform" in audio:
                samples = audio["waveform"]
            else:
                raise ValueError("Input audio dict contains neither 'samples' nor 'waveform'")
                
            sample_rate = audio["sample_rate"]
            
        except Exception as e:
            print(f"[ElevenLabs Node] FATAL: Could not read input audio. Error: {e}")
            return (f"FATAL: Could not read input audio. Error: {e}",)
        
        # --- Save Input Audio to Temp File (with all fixes) ---
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_file_path = temp_file.name
        temp_file.close()

        try:
            # Fix for 3D tensors
            if samples.ndim == 3:
                samples_2d = samples[0]
            else:
                samples_2d = samples 

            torchaudio.save(temp_file_path, samples_2d.cpu(), sample_rate)
            
            # --- Call ElevenLabs API ---
            url = f"https://api.elevenlabs.io/v1/speech-to-speech/{voice_id}?output_format=mp3_44100_128"
            headers = { "xi-api-key": api_key }
            data = { "model_id": "eleven_multilingual_sts_v2" }

            try:
                with open(temp_file_path, "rb") as audio_file:
                    files = { "audio": (os.path.basename(temp_file_path), audio_file, "audio/mpeg") }
                    print(f"[ElevenLabs Node] Sending STS request...")
                    response = requests.post(url, headers=headers, data=data, files=files)
                    response.raise_for_status() 

                    # --- Save API Response to FINAL file ---
                    output_dir = "output"
                    os.makedirs(output_dir, exist_ok=True) 
                    timestamp = int(time.time())
                    output_filename = f"sts_output_{timestamp}.mp3"
                    output_save_path = os.path.join(output_dir, output_filename)

                    with open(output_save_path, "wb") as f:
                        f.write(response.content)

                    print(f"[ElevenLabs Node] Success! Audio saved to: {output_save_path}")

                    # --- Return the FINAL file path ---
                    return (output_save_path,)

            except requests.exceptions.HTTPError as e:
                print(f"[ElevenLabs Node] HTTP Error: {e.response.text}")
                return (f"HTTP Error: {e.response.text}",)
            except Exception as e:
                print(f"[ElevenLabs Node] General Error: {e}")
                return (f"General Error: {e}",)

        finally:
            # Clean up the *input* temp file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)