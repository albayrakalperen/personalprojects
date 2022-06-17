from google.cloud import texttospeech
from PyPDF2 import PdfReader
import os

credential_path = r"C:\Users\zornd\Downloads\YOUR_JSON_FILE.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

reader = PdfReader(r"C:\Users\zornd\Desktop\PDF_FILE.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[5]
text = page.extract_text()

memory_full_text = reader.pages[25].extract_text()

client = texttospeech.TextToSpeechClient()
synthesis_input = texttospeech.SynthesisInput(text=memory_full_text)

voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')


