import streamlit as st
import edge_tts
import asyncio
import tempfile

st.set_page_config(page_title="Lektor Notatek", layout="centered")

st.header("🎧 Twój Osobisty Lektor (Wersja Poprawiona)")

text = st.text_area("Wpisz tekst tutaj:", height=250, placeholder="Wklej notatki...")

voice = st.selectbox(
    "Wybierz lektora:",
    ["pl-PL-MarekNeural", "pl-PL-ZofiaNeural"]
)

rate_str = st.select_slider("Prędkość:", options=["-50%", "-25%", "+0%", "+25%", "+50%"], value="+0%")

# --- TO JEST CZĘŚĆ NAPRAWIAJĄCA BŁĄD ---
async def generate_audio_file(text, voice, rate, output_file):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_file)

def run_async_task(text, voice, rate, output_file):
    # Tworzymy nową pętlę zdarzeń specjalnie dla tego zadania
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(generate_audio_file(text, voice, rate, output_file))
    finally:
        loop.close()
# ---------------------------------------

if st.button("🚀 Generuj MP3", use_container_width=True):
    if text:
        with st.spinner("Generowanie..."):
            try:
                # Tworzymy plik tymczasowy
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    temp_filename = fp.name
                
                # Uruchamiamy funkcję w bezpieczny sposób
                run_async_task(text, voice, rate_str, temp_filename)
                
                st.success("Gotowe!")
                
                # Odtwarzacz
                st.audio(temp_filename, format='audio/mp3')
                
                # Pobieranie
                with open(temp_filename, "rb") as file:
                    st.download_button(
                        label="📥 Pobierz MP3",
                        data=file,
                        file_name="notatki.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Wystąpił błąd: {e}")
    else:
        st.warning("Najpierw wpisz tekst!")
