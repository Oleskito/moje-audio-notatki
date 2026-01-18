import streamlit as st
import edge_tts
import asyncio
import io

st.set_page_config(page_title="Lektor Notatek", layout="centered")

st.header("🎧 Lektor (Wersja iOS Safe)")

text = st.text_area("Wpisz tekst tutaj:", height=250, placeholder="Wklej notatki...")

voice = st.selectbox(
    "Wybierz lektora:",
    ["pl-PL-MarekNeural", "pl-PL-ZofiaNeural"]
)

rate_str = st.select_slider("Prędkość:", options=["-50%", "-25%", "+0%", "+25%", "+50%"], value="+0%")

async def generate_audio_stream(text, voice, rate):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    # Zbieramy dane audio do bufora w pamięci (RAM) zamiast do pliku
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

def get_audio_bytes(text, voice, rate):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(generate_audio_stream(text, voice, rate))
    finally:
        loop.close()

if st.button("🚀 Generuj MP3", use_container_width=True):
    if text:
        with st.spinner("Generowanie..."):
            try:
                # Pobieramy bajty bezpośrednio
                audio_bytes = get_audio_bytes(text, voice, rate_str)
                
                st.success("Gotowe!")
                
                # Odtwarzacz z bajtów
                st.audio(audio_bytes, format='audio/mp3')
                
                # Pobieranie z bajtów
                st.download_button(
                    label="📥 Pobierz MP3",
                    data=audio_bytes,
                    file_name="notatki.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Błąd: {e}")
    else:
        st.warning("Najpierw wpisz tekst!")
