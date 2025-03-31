# from googletrans import Translator
# from gtts import gTTS
# import os


# # Get the base directory where the script is located
# base_dir = os.path.abspath(os.path.dirname(__file__))

# # Create the output path in the correct directory
# output_dir = os.path.abspath(os.path.join(base_dir, "..", "output"))

# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)


# # Generate Hindi TTS
# def generate_tts(text, output_path=None):
#     """Generate Hindi TTS from translated text and save to output directory."""
#     if not text:
#         return None

#     try:
#         # Set the correct output path if not provided
#         if output_path is None:
#             output_path = os.path.join(output_dir, "hindi_tts_output.mp3")

#         # Generate and save the TTS
#         tts = gTTS(text=text, lang="hi")
#         tts.save(output_path)

#         return output_path
#     except Exception as e:
#         return None



# # Translate to Hindi
# def translate_to_hindi(text):
#     """Translate English text to Hindi using Google Translator."""
#     try:
#         translator = Translator()
#         translation = translator.translate(text, dest="hi")

#         if translation and translation.text:
#             return translation.text
#         else:
#             return None
#     except Exception as e:
#         return None

# # Process and Generate TTS
# def process_and_generate_tts(text, audio_path=None):
#     """Translate and generate Hindi TTS, with optional audio path."""
#     if not text:
#         return None

#     # Translate to Hindi
#     hindi_text = translate_to_hindi(text)

#     if hindi_text:
#         # Generate TTS and save it to specified path
#         if audio_path is None:
#             audio_path = os.path.join(output_dir, "hindi_tts_output.mp3")

#         audio_path = generate_tts(hindi_text, audio_path)

#         # Check if audio is saved successfully
#         if audio_path and os.path.exists(audio_path):
#             return audio_path
#         else:
#             return None
#     else:
#         return None

#---------------------------------------------------------------------------------
#success running code using docker 

import asyncio
from googletrans import Translator
from gtts import gTTS
import os

# Get the base directory where the script is located
base_dir = os.path.abspath(os.path.dirname(__file__))

# Create the output path in the correct directory
output_dir = os.path.abspath(os.path.join(base_dir, "..", "output"))

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# Generate Hindi TTS
def generate_tts(text, output_path=None):
    """Generate Hindi TTS from translated text and save to output directory."""
    if not text:
        return None

    try:
        # Set the correct output path if not provided
        if output_path is None:
            output_path = os.path.join(output_dir, "hindi_tts_output.mp3")

        # Generate and save the TTS
        tts = gTTS(text=text, lang="hi")
        tts.save(output_path)

        return output_path
    except Exception as e:
        print(f"❌ TTS generation failed: {e}")
        return None


# Translate to Hindi - NOW ASYNC ✅
async def translate_to_hindi(text):
    """Translate English text to Hindi using Google Translator."""
    try:
        loop = asyncio.get_event_loop()
        translator = Translator()
        # Run translation asynchronously
        translation = await loop.run_in_executor(None, translator.translate, text, "hi")

        if translation and translation.text:
            return translation.text
        else:
            return None
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return None


# Process and Generate TTS
async def process_and_generate_tts(text, audio_path=None):
    """Translate and generate Hindi TTS, with optional audio path."""
    if not text:
        return None

    # Translate to Hindi
    hindi_text = await translate_to_hindi(text)

    if hindi_text:
        # Generate TTS and save it to specified path
        if audio_path is None:
            audio_path = os.path.join(output_dir, "hindi_tts_output.mp3")

        audio_path = generate_tts(hindi_text, audio_path)

        # Check if audio is saved successfully
        if audio_path and os.path.exists(audio_path):
            return audio_path
        else:
            return None
    else:
        return None


