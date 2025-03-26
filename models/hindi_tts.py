from googletrans import Translator
from gtts import gTTS
import os


# Ensure 'output' directory exists
if not os.path.exists("output"):
    os.makedirs("output")


def generate_tts(text, output_path="output/hindi_tts_output.wav"):
    """Generate Hindi TTS from translated text."""
    try:
        print(f"Input text: {text}")  # Debug the input text
        tts = gTTS(text=text, lang="hi")
        tts.save(output_path)

        print(f"TTS generated successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None


def translate_to_hindi(text):
    """Translate English text to Hindi."""
    try:
        translator = Translator()
        translation = translator.translate(text, dest="hi")
        print(f"Translated text: {translation.text}")  # Debug translation
        return translation.text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None


def process_and_generate_tts(text):
    """Translate and generate Hindi TTS."""
    hindi_text = translate_to_hindi(text)
    if hindi_text:
        return generate_tts(hindi_text)
    else:
        print("Failed to generate audio due to translation error.")
        return None

