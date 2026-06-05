import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

duration = 5 # durasi rekaman dalam detik
sample_rate = 44100

words_by_level = {
    "mudah": ["kucing", "anjing", "apel", "susu", "matahari"],
    "sedang": ["pisang", "sekolah", "teman", "jendela", "kuning"],
    "sulit": ["teknologi", "universitas", "informasi", "pengucapan", "imajinasi"],
    "expert": ["karakteristik", "restorasi", "eksplorasi", "infrastruktur", "termodinamika"]
}


total_score = 0

point_rewards = {
    "mudah": 10,
    "sedang": 20,
    "sulit": 30,
    "expert": 50
}

while True:
    print(f"🏆 Skor Kamu Saat Ini: {total_score}")
    print("Pilih tingkat kesulitan: (🟢mudah/🟡sedang/🔴sulit/👑expert)")
    level = input(">>>")
    if level =='exit':
        break
    #kata random yang nanti harus kita terjemahin ketika record ke bahasa jepang
    word = random.choice(words_by_level[level])
    print(f"ucapkan kata {word} dalam bahasa jepang")

    #rekam suara
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
        text = recognizer.recognize_google(audio, language="ja-JP")
        print("Kamu mengatakan :", text)
        translator = Translator()
        translated = translator.translate(word, src='id',dest='ja').text.lower()  # Kode 'ja' adalah kode untuk bahasa jepang
        print("🌍 Terjemahan ke Bahasa Jepang:", translated)

        if translated == text:
            earned_points = point_rewards[level]
            total_score += earned_points
            print(f"🎉 Selamat kamu benar! (+{earned_points} poin)")
        else:
            print("Maaf, Jawabanmu salah.")
            total_score -= point_rewards[level]
            if total_score < 0:
                print("💀GameOver! Skor kamu sudah 0.💀")
                break
    except sr.UnknownValueError:             # - jika Google tidak dapat mengenali suara karena bising atau sepi
        print("Suara tidak dapat dikenali")
    except sr.RequestError as e:             # - jika tidak ada koneksi internet atau API tidak tersedia
        print(f"Service error: {e}")