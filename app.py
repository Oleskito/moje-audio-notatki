import streamlit as st
import edge_tts
import asyncio
import tempfile
import os

# Konfiguracja strony (żeby ładnie wyglądała na telefonie)
st.set_page_config(page_title="Lektor Notatek", layout="centered")

st.header("🎧 Twój Osobisty Lektor")
st.markdown("Wklej notatki, a ja zrobię z nich MP3.")

# Pole tekstowe
text = st.text_area("Wpisz tekst tutaj:", height=250, placeholder="Np. Inflacja to proces wzrostu cen...")

# Wybór głosu
voice = st.selectbox(
    "Wybierz lektora:",
    ["pl-PL-MarekNeural", "pl-PL-ZofiaNeural"],
    index=0
)

# Suwak prędkości (opcjonalnie, domyślnie +0%)
rate_str = st.select_slider("Prędkość:", options=["-50%", "-25%", "+0%", "+25%", "+50%"], value="+0%")

async def text_to_speech(text, voice, rate, output_file):
    # Konwersja prędkości na format wymagany przez edge-tts
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_file)

if st.button("🚀 Generuj MP3", use_container_width=True):
    if text:
        with st.spinner("Lektor czyta... to potrwa chwilę..."):
            try:
                # Tworzenie pliku tymczasowego
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    temp_filename = fp.name
                
                # Uruchomienie asynchroniczne
                asyncio.run(text_to_speech(text, voice, rate_str, temp_filename))
                
                st.success("Gotowe!")
                
                # Odtwarzacz
                st.audio(temp_filename, format='audio/mp3')
                
                # Przycisk pobierania
                with open(temp_filename, "rb") as file:
                    btn = st.download_button(
                        label="📥 Pobierz plik na telefon",
                        data=file,
                        file_name="notatki_audio.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"Wystąpił błąd: {e}")
    else:
        st.warning("Najpierw wklej jakiś tekst!")
