# 🎙️ Agentic AI Interview Partner

**A Context-Aware, Voice-Enabled Technical Interviewer that adapts to you.**

> **Submission for:** Eightfold.ai AI Agent Assignment  
> **Built by:** Shanigarapu Abhinav  

---

## 📖 Project Overview
Most mock interview bots are static—they ask generic questions without knowing who you are. I built the **Agentic Interview Partner** to solve this.

Unlike standard chatbots, this agent uses a **State-Machine Architecture**. It reads your **actual PDF Resume**, compares it against a specific **Job Description**, and conducts a structured interview to find gaps in your knowledge.

### 🌟 Key Features
* **📄 Context-Aware Intelligence:** Performs real-time "Gap Analysis" between your Resume and the Job Description to ask relevant questions.
* **🗣️ Neural Voice Interaction:** Uses **Microsoft Edge TTS** for human-like speech (no robotic voices).
* **🧠 Agentic Reasoning:** Includes a **Hint System** that acts as a mentor, providing clues to unblock confused candidates.
* **📊 Actionable Feedback:** Generates a structured Competency Scorecard (Markdown) rating your Communication and Technical depth.

---

## 🏗️ Architecture & Design Decisions

To meet the requirement of "Agentic Behaviour," I avoided a simple Q&A loop and focused on User Experience.

### 1. Context Injection (RAG-Lite)
* **The Problem:** Generic questions (e.g., "What is Python?") are useless for senior roles.
* **The Solution:** I implemented a dynamic system prompt that ingests the **PDF Resume text** at runtime. The LLM performs a retrieval task to validate specific skills mentioned in the resume against the job requirements.

### 2. Voice Architecture & User Control
* **Decision:** I prioritized a "Voice-First" experience but realized that **latency and interruption** are major challenges in web-based AI.
* **The Fix:**
    1.  **Quality:** Integrated `edge-tts` for natural, non-robotic audio.
    2.  **Control:** I implemented a **"Stop Speaking" button** and custom JavaScript. This solves the "Barge-In" problem, allowing users who read faster than the AI speaks to silence the audio instantly and proceed at their own pace.

### 3. Handling User Personas
* **The Confused User:** Instead of letting a candidate fail silently, I added a **Hint Button**. This triggers a parallel LLM call to provide a scaffolding clue.
* **The Chatty User:** The System Prompt includes strict **Guardrails** to politely deflect off-topic conversation (e.g., asking for pizza) and steer back to the interview.
* **The Efficient User:** The model temperature (`0.7`) is tuned to recognize concise, correct answers and immediately ramp up the difficulty.

---

## 🛠️ Setup Instructions

### Prerequisites
* Python 3.10+
* A Google Gemini API Key (Free Tier)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone [YOUR_GITHUB_REPO_LINK]
    cd InterviewBot
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Credentials**
    * Create a file named `.env` in the root directory.
    * Add your API key:
        ```text
        GOOGLE_API_KEY=your_actual_api_key_here
        ```

4.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

---

## 🚀 How to Use
1.  **Upload Resume:** Upload your PDF resume in the sidebar.
2.  **Configure Role:** Enter the target Job Role and Description.
3.  **Start:** Click **Start Interview**.
4.  **Interact:** Use the Microphone for voice answers or type text.
    * *Use the "Stop Speaking" button to interrupt the AI if needed.*
5.  **Finish:** Click **Finish & Get Feedback** to generate and download your Scorecard.

---

## 🤖 Tech Stack
* **Frontend:** Streamlit
* **Orchestration:** LangChain
* **LLM:** Google Gemini 2.0 Flash-Lite (Optimized for speed)
* **Audio:** Edge-TTS (Neural Voice), SpeechRecognition
* **PDF Processing:** PyPDF