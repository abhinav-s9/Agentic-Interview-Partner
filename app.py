import streamlit as st
from agent import InterviewAgent
import io
from pypdf import PdfReader
import speech_recognition as sr
import base64
import asyncio
import edge_tts

# Page Config
st.set_page_config(page_title="Eightfold Agentic Interviewer", layout="wide", page_icon="🎙️")

# --- JAVASCRIPT: TRY TO STOP AUDIO ON CLICKS ---
# This attempts to stop audio. If it fails due to security, the "Stop Button" is the backup.
st.markdown("""
<script>
    function stopAllAudio() {
        var audios = document.querySelectorAll('audio');
        audios.forEach(function(audio) {
            audio.pause();
            audio.currentTime = 0;
        });
    }
    // Try to listen to the main document
    document.addEventListener('click', stopAllAudio, true);
    document.addEventListener('keydown', stopAllAudio, true);
    document.addEventListener('touchstart', stopAllAudio, true);
</script>
""", unsafe_allow_html=True)

# --- Custom CSS ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 10px; padding: 10px; }
    .stButton button { width: 100%; border-radius: 5px; height: 45px; font-size: 16px; }
    .instruction-card { background-color: #1E1E1E; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B; }
    .feedback-box { background-color: #262730; padding: 20px; border-radius: 10px; border: 1px solid #4CAF50; }
    </style>
    """, unsafe_allow_html=True)


# --- Edge TTS ---
async def generate_audio_stream(text):
    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data


def text_to_speech(text):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_bytes = loop.run_until_complete(generate_audio_stream(text))
        return io.BytesIO(audio_bytes)
    except Exception as e:
        return None


# --- SMART AUDIO RENDERER ---
def render_audio(audio_buffer, msg_index, audio_mode, is_last_message):
    if audio_buffer:
        is_new = msg_index not in st.session_state.played_indices
        if is_new:
            st.session_state.played_indices.add(msg_index)

        should_autoplay = audio_mode and is_new and is_last_message

        data = audio_buffer.getvalue()
        b64 = base64.b64encode(data).decode()

        # Unique ID
        aid = f"audio-{msg_index}"

        if should_autoplay:
            # We inject a specific script right next to the player to monitor ITSELF
            md = f"""
                <audio id="{aid}" autoplay style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)


# --- Helpers ---
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text if text else "Resume text could not be extracted."
    except Exception as e:
        return f"Error reading PDF: {e}"


def transcribe_audio(audio_bytes):
    r = sr.Recognizer()
    try:
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language='en-IN')
            return text
    except:
        return "Error"


# --- Session State ---
if "agent" not in st.session_state:
    st.session_state.agent = InterviewAgent()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "interview_active" not in st.session_state:
    st.session_state.interview_active = False
if "feedback_generated" not in st.session_state:
    st.session_state.feedback_generated = False
if "played_indices" not in st.session_state:
    st.session_state.played_indices = set()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=50)
    st.title("Configuration")

    # Mode Toggle
    audio_mode = st.toggle("🔊 Enable Audio Response", value=True)
    if not audio_mode:
        st.caption("Chat Mode (Silent)")
    else:
        st.caption("Voice Mode (Auto-Speak)")

    # THE RELIABLE STOP BUTTON
    # This forces a page reload, which kills all audio immediately.
    if st.button("🔇 STOP SPEAKING", type="secondary", use_container_width=True):
        st.rerun()

    st.divider()

    uploaded_file = st.file_uploader("1. Upload Resume (PDF)", type="pdf")
    resume_text = extract_text_from_pdf(uploaded_file) if uploaded_file else ""
    if uploaded_file:
        st.success("✅ Resume Loaded")

    st.divider()

    role = st.text_input("2. Target Role", "Full Stack Developer")
    level = st.selectbox("3. Seniority", ["Junior", "Mid-Level", "Senior"])
    job_desc = st.text_area("4. Job Description", "Must know Python, React, and AWS.", height=100)

    st.divider()

    if not st.session_state.interview_active:
        if st.button("🚀 Start Interview", type="primary"):
            st.session_state.interview_active = True
            st.session_state.chat_history = []
            st.session_state.played_indices = set()
            st.session_state.feedback_generated = False

            with st.spinner("AI is analyzing your profile..."):
                msg = st.session_state.agent.start_interview(role, level, job_desc, resume_text)

            audio = text_to_speech(msg)
            st.session_state.chat_history.append({"role": "ai", "content": msg, "audio": audio})
            st.rerun()
    else:
        if st.button("🏁 Finish & Get Feedback", type="primary"):
            if len(st.session_state.chat_history) < 5:
                st.error("⚠️ Please answer at least 2 questions!")
            else:
                with st.spinner("Generating Report..."):
                    feedback = st.session_state.agent.generate_final_report()
                    st.session_state.chat_history.append({"role": "ai", "content": feedback, "is_feedback": True})
                    st.session_state.feedback_generated = True
                    st.session_state.interview_active = False
                st.rerun()

    if st.button("🔄 Reset"):
        st.session_state.interview_active = False
        st.session_state.feedback_generated = False
        st.session_state.chat_history = []
        st.session_state.played_indices = set()
        st.rerun()

# --- MAIN UI ---
if not st.session_state.interview_active and not st.session_state.feedback_generated:
    st.title("👋 Welcome to AI Interview Partner")
    st.markdown("### *Master your interview skills with Agentic AI.*")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="instruction-card">
        <h3>How to use:</h3>
        <ol>
            <li><strong>Upload your Resume</strong> in the sidebar.</li>
            <li><strong>Set the Job Role</strong>.</li>
            <li>Click <span style="color: #FF4B4B;"><b>Start Interview</b></span>.</li>
            <li>Click <span style="color: #FF4B4B;"><b>Finish</b></span> to get your Scorecard.</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.info("ℹ️ **Tip:** Allow microphone access.")

else:
    st.title(f"🎙️ Interviewing for: {role}")

    chat_container = st.container()
    with chat_container:
        total_messages = len(st.session_state.chat_history)
        for i, msg in enumerate(st.session_state.chat_history):
            if msg.get("is_feedback"):
                st.markdown(f"<div class='feedback-box'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                avatar = "🤖" if msg["role"] == "ai" else "👤"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.write(msg["content"])
                    if msg.get("audio"):
                        is_last_message = (i == total_messages - 1)
                        render_audio(msg["audio"], i, audio_mode, is_last_message)

    if st.session_state.feedback_generated:
        st.divider()
        final = st.session_state.chat_history[-1]["content"]
        st.download_button("📥 Download Report", final, "Scorecard.md")

    if st.session_state.interview_active:
        st.divider()
        input_container = st.container()
        with input_container:
            c1, c2, c3 = st.columns([3, 1, 0.5])
            with c1:
                text_input = st.chat_input("Type your answer...")
            with c2:
                audio_input = st.audio_input("Mic")
            with c3:
                if st.button("💡 Hint?"):
                    with st.spinner("Thinking..."):
                        hint_msg = st.session_state.agent.provide_hint()
                        audio = text_to_speech(hint_msg)
                        st.session_state.chat_history.append(
                            {"role": "ai", "content": f"**HINT:** {hint_msg}", "audio": audio})
                        st.rerun()

            if "last_audio_bytes" not in st.session_state:
                st.session_state.last_audio_bytes = None
            user_input = None

            if audio_input:
                audio_bytes = audio_input.read()
                if audio_bytes and audio_bytes != st.session_state.last_audio_bytes:
                    st.session_state.last_audio_bytes = audio_bytes
                    with st.spinner("Transcribing..."):
                        text = transcribe_audio(audio_bytes)
                        if "Error" not in text:
                            st.success(f"🎙️ Heard: '{text}'")
                            user_input = text
                        else:
                            st.warning("Could not hear you.")

            if text_input: user_input = text_input

            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.spinner("Interviewer is thinking..."):
                    response = st.session_state.agent.process_response(user_input)
                audio = text_to_speech(response)
                st.session_state.chat_history.append({"role": "ai", "content": response, "audio": audio})
                st.rerun()