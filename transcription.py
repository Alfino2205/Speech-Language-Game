import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

duration = 5  # durasi rekaman dalam detik
sample_rate = 44100

print("Speak now...")
recording = sd.rec(
  int(duration * sample_rate), # jumlah contoh rekaman
  samplerate=sample_rate,      # sample rate
  channels=1,                  # 1 berarti rekaman tunggal
  dtype="int16")               # tipe data untuk contoh rekaman
sd.wait()  # menunggu rekaman selesai

wav.write("output.wav", sample_rate, recording)
print("Rekaman selesai, memulai pengenalan suara...")

recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)



try:
    text = recognizer.recognize_google(audio, language="id-ID")
    print("Kamu mengatakan :", text)
    print("Contoh kode bahasa: 'it' (Italia), 'es' (Spanyol), 'ja' (Jepang), 'en' (Inggris)")
    lang = input("Ingin diterjemahkan ke bahasa apa?: ").strip().lower()
    translator = Translator()
    translated = translator.translate(text, dest=lang)  # Kode 'es' adalah kode untuk bahasa Spanyol
    print(f"🌍 Terjemahan ke {lang}: {translated.text}")
except sr.UnknownValueError:             # - jika Google tidak dapat mengenali suara karena bising atau sepi
    print("Suara tidak dapat dikenali")
except sr.RequestError as e:             # - jika tidak ada koneksi internet atau API tidak tersedia
    print(f"Service error: {e}")


