# pip install SpeechRecognition
# Librerías
import json
import nltk
import streamlit as st
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pytube import YouTube
import moviepy.editor as mp

# Cargar el conjunto de palabras consideradas violentas desde un archivo JSON
with open("palabrasvio.json") as f:
    violent_words = json.load(f)

# Configurar el reconocedor de voz
r = sr.Recognizer()

# Proceso NLP
nltk.download("punkt")
nltk.download("stopwords")

# SIMILITUDES


# Definir el índice de Tversky
def tversky_index(set_a, set_b, alpha=0.1, beta=0.1):
    intersect = len(set_a.intersection(set_b))
    diff_ab = len(set_a.difference(set_b))
    diff_ba = len(set_b.difference(set_a))

    index = intersect / (intersect + alpha * diff_ab + beta * diff_ba)

    return index


# Definir el índice de Jaccard
def jaccard_index(set_a, set_b):
    intersect = set_a.intersection(set_b)
    union = set_a.union(set_b)

    index = len(intersect) / len(union)

    return index


# Definir el índice de Sørensen-Dice.
def sorensen(set_a, set_b):
    intersect = set_a.intersection(set_b)
    index = 2 * len(intersect) / (len(set_a) + len(set_b))

    return index


# Cargar el conjunto de palabras consideradas violentas desde un archivo JSON
with open("palabrasvio.json") as f:
    violent_words = json.load(f)

# Conjunto de palabras violentas
set_violent = set(violent_words)


# Título de la página
st.title("Detector de Malas Palabras en Audios")

# subir audio en caso se requiera
# Subir archivo de audio
audio_subido = st.sidebar.file_uploader("Sube un archivo de audio:", type=["wav"])

if audio_subido:
    try:
        with sr.AudioFile(audio_subido) as source:
            st.write("Leyendo el archivo de audio...")
            audio = r.record(source)

        text = r.recognize_google(audio, language="es-ES")
        st.write("Texto reconocido del audio:")
        st.write(text)

        # Tokenizar el texto
        tokens = word_tokenize(text)

        # Filtrar las stopwords
        stop_words = set(stopwords.words("spanish"))
        filtered_tokens = [word for word in tokens if word.casefold() not in stop_words]

        # Convertir tokens en un conjunto para eliminar duplicados
        set_tokens = set(filtered_tokens)

        # Calcular y mostrar los índices de Tversky y Jaccard
        tversky = tversky_index(set_violent, set_tokens)  # DAR PARAMETROS
        jaccard = jaccard_index(set_violent, set_tokens)  # DAR PARAMETROS
        sorensen_Dice = sorensen(set_violent, set_tokens)  # DAR PARAMETROS

        st.write("Índice de Tversky:", tversky)
        st.write("Índice de Jaccard:", jaccard)
        st.write("Índice de Sørensen-Dice:", sorensen_Dice)
    # error aun no se descargo ningun audio
    except FileNotFoundError:
        st.sidebar.warning(
            "Esperando a que se descargue un archivo de audio de youtube..."
        )
    except sr.UnknownValueError:
        st.error("Google Speech Recognition no pudo entender el audio")
    except sr.RequestError as e:
        st.error(
            f"No se pudieron solicitar resultados del servicio de reconocimiento de voz de Google; {e}"
        )


st.sidebar.title("Descargar y Convertir Audio de YouTube a WAV")

# Ingresar la URL de YouTube
youtube_url = st.sidebar.text_input("Ingresa la URL de YouTube:")

if youtube_url:
    try:
        # Crear una instancia de YouTube con la URL
        yt = YouTube(youtube_url)

        # Obtener la mejor calidad de audio
        audio_stream = yt.streams.filter(only_audio=True).first()

        if audio_stream:
            # Descargar el audio
            audio_stream.download(filename="audio.mp4")

            # Convertir el audio descargado a formato WAV
            clip = mp.AudioFileClip("audio.mp4")
            clip.write_audiofile("audio.wav")

            st.sidebar.success(f"¡Audio descargado y convertido a WAV exitosamente!")
            st.sidebar.audio("audio.wav", format="audio/wav")
        else:
            st.error("No se encontraron streams de audio para esta URL.")
    except Exception as e:
        st.error(f"Ocurrió un error al descargar el audio: {str(e)}")


uploaded_audio = "audio.wav"

if uploaded_audio:
    try:
        with sr.AudioFile(uploaded_audio) as source:
            st.write("Leyendo el archivo de audio...")
            audio = r.record(source)

        text = r.recognize_google(audio, language="es-ES")
        st.write("Texto reconocido del audio:")
        st.write(text)

        # Tokenizar el texto
        tokens = word_tokenize(text)

        # Filtrar las stopwords
        stop_words = set(stopwords.words("spanish"))
        filtered_tokens = [word for word in tokens if word.casefold() not in stop_words]

        # Convertir tokens en un conjunto para eliminar duplicados
        set_tokens = set(filtered_tokens)

        # Calcular y mostrar los índices de Tversky y Jaccard
        tversky = tversky_index(set_violent, set_tokens)  # DAR PARAMETROS
        jaccard = jaccard_index(set_violent, set_tokens)  # DAR PARAMETROS
        sorensen_Dice = sorensen(set_violent, set_tokens)  # DAR PARAMETROS

        st.write("Índice de Tversky:", tversky)
        st.write("Índice de Jaccard:", jaccard)
        st.write("Índice de Sørensen-Dice:", sorensen_Dice)
    # error aun no se descargo ningun audio
    except FileNotFoundError:
        st.sidebar.warning(
            "Esperando a que se descargue un archivo de audio de youtube..."
        )
    except sr.UnknownValueError:
        st.error("Google Speech Recognition no pudo entender el audio")
    except sr.RequestError as e:
        st.error(
            f"No se pudieron solicitar resultados del servicio de reconocimiento de voz de Google; {e}"
        )
