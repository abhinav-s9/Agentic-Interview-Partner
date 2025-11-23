import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

class InterviewAgent:
    def __init__(self):
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-lite",
                google_api_key=api_key,
                temperature=0.7
            )
        except Exception:
            self.llm = None
        self.history = []

    def start_interview(self, role, level, job_desc, resume_text):
        self.history = []
        instruction = f"""
        ROLE: You are a Friendly but Professional Technical Recruiter for {role} ({level}).
        CONTEXT: Job Description: "{job_desc}". Resume: "{resume_text}".
        GOAL: Validate skills.
        RULES: Be Human. One Question at a time. Probe vague answers. Stay on track.
        USER: I am ready. Begin.
        """
        self.history.append(HumanMessage(content=instruction))
        return self._invoke()

    def process_response(self, user_input):
        self.history.append(HumanMessage(content=user_input))
        return self._invoke()

    def provide_hint(self):
        prompt = "The candidate is stuck. Provide a short, helpful hint for the last question. Do NOT give the answer."
        self.history.append(HumanMessage(content=prompt))
        return self._invoke()

    def generate_final_report(self):
        prompt = """
        The interview is finished. Generate a detailed Feedback Report in Markdown.
        Structure: Candidate Summary, Communication Skills (/10), Technical Knowledge (/10), Strengths, Areas for Improvement, Final Verdict.
        """
        self.history.append(HumanMessage(content=prompt))
        return self._invoke()

    def _invoke(self):
        try:
            res = self.llm.invoke(self.history)
            self.history.append(res)
            return res.content
        except Exception as e:
            return f"Error: {e}"