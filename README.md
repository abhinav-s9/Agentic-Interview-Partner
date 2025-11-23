# 🎙️ Agentic AI Interview Partner

### *A Context-Aware, Voice-Enabled Technical Interviewer*

> **Submission for:** Eightfold.ai AI Agent Assignment  
> **Built by:** Shanigarapu Abhinav  

---

## 📖 Project Overview
The **Agentic Interview Partner** is designed to solve the problem of static, generic mock interviews. Unlike standard chatbots, this agent utilizes a **State-Machine Architecture** to conduct a structured, multi-modal interview tailored specifically to the candidate's resume and target job description.

### 🌟 Key Features
* **📄 Context-Aware Intelligence:** Parses the candidate's actual **PDF Resume** and performs a real-time Gap Analysis against the Job Description.
* **🗣️ Voice-First Interaction:** Features **Microsoft Edge Neural TTS** for human-like speech.
* **🧠 Agentic Reasoning:** Includes a **Hint System** that scaffolds learning for confused candidates instead of just giving answers.
* **📊 Actionable Feedback:** Generates a structured Competency Scorecard (Markdown) with specific grading on Communication and Technical depth.

---

## 🏗️ Architecture & Design Decisions

To meet the requirement of "Agentic Behaviour," I avoided a simple Q&A loop.

### 1. Context Injection
* **Decision:** Instead of generic questions, the agent ingests the candidate's **Real Resume (PDF)** and the **Job Description** at runtime.
* **Reasoning:** This allows the agent to perform **Gap Analysis**—asking questions specifically about skills missing from the resume but required by the job.

### 2. Voice Architecture with "Kill Switch"
* **Decision:** Integrated **Microsoft Edge TTS (Neural Voice)** over standard gTTS for a more professional persona.
* **Technical Challenge:** Streamlit audio players typically "loop" or overlap on page reloads.
* **Solution:** I implemented a custom **JavaScript Event Listener** that listens for `mousedown` events to silence audio immediately when the user interacts. This simulates a natural "Barge-In" experience found in real phone calls.

### 3. User Persona Handling
* **The Confused User:** Implemented a **Hint System** to unblock candidates without revealing answers.
* **The Chatty User:** System Prompts include **Guardrails** to politely deflect off-topic conversation.
* **The Efficient User:** The model temperature (`0.7`) is tuned to recognize concise answers and increase difficulty dynamically.

### 4. State Management
* **Decision:** Used `st.session_state` to enforce a strict flow (Landing Page -> Interview -> Feedback).
* **Reasoning:** Prevents logical errors (e.g., asking for feedback before the interview starts) and ensures a clean UI.

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
3.  **Start:** Click "Start Interview".
4.  **Interact:** Use the Microphone for voice answers or type text.
5.  **Finish:** Click "Finish & Get Feedback" to download your Scorecard.

---

## 🤖 Tech Stack
* **Frontend:** Streamlit
* **Orchestration:** LangChain
* **LLM:** Google Gemini 2.0 Flash-Lite
* **Audio:** Edge-TTS (Neural Voice), SpeechRecognition
* **PDF Processing:** PyPDF