import os
import markdown2
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from groq import Groq
from dotenv import load_dotenv

# Load your API key
load_dotenv()
app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head><title>StudyBuddy AI</title></head>
    <body style="font-family: sans-serif; text-align: center; padding: 50px;">
        <h1>StudyBuddy AI</h1>
        <form action="/ask" method="post">
            <input type="text" name="question" placeholder="Ask me anything..." required style="padding: 10px; width: 300px;">
            <button type="submit">Ask AI</button>
        </form>
    </body>
    </html>
    """

@app.post("/ask", response_class=HTMLResponse)
def ask_ai(question: str = Form(...)):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": question}]
        )
        # Convert raw AI text to beautiful formatted text
        raw_content = completion.choices[0].message.content
        ai_response = markdown2.markdown(raw_content)
    except Exception as e:
        ai_response = f"Oops! Something went wrong: {str(e)}"
    
    return f"""
    <html>
    <body style="font-family: sans-serif; padding: 50px;">
        <h3>Your Question: {question}</h3>
        <hr>
        <div>{ai_response}</div>
        <br>
        <a href="/">← Ask another</a>
    </body>
    </html>
    """
