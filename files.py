import speech_recognition as sr

r = sr.Recognizer()


def listen_com():
    audio_file = sr.AudioFile(r'C:\Users\alexv\OneDrive\Документы\Аудиозаписи\Запись1.wav')
    with audio_file as source:
        try:
            audio = r.listen(source)
            command = r.recognize_google(audio, language='ru-RU')
        except sr.UnknownValueError:
            return ''
        return command


print(listen_com())
