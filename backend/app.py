# omkaaaaaar/student-support-agent/student-support-agent-2d56a55ed0ee20653db24666d91898d4734f10a6/backend/app.py
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv # For loading API key from .env file

# Import Langchain components
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables (this will load GEMINI_API_KEY from a .env file if present)
load_dotenv()

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# --- Configure the LLM with Langchain ---
try:
    # Get the API key from environment variables
    # For local development, create a .env file in your 'backend' directory with:
    # GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it.")

    # Initialize the Gemini LLM model
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key) # You can use "gemini-1.5-flash" or "gemini-pro"
    
    # Define your prompt template using Langchain's ChatPromptTemplate
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are an AI-powered student support agent for an online course.
        Your goal is to answer student questions accurately and concisely.
        The course covers topics such as Python Programming, Full-Stack Web Development,
        and AI Agent Development.
        
        If you don't know the answer, politely state that you cannot find the information and suggest
        they contact support via email at support@scoreazy.com or by calling +1-800-555-0199 during
        business hours (9 AM - 5 PM PST, Monday-Friday).
        
        Common inquiries also include:
        - Course timing/schedule (e.g., Live sessions are Mon/Wed at 5 PM PST. Recordings available in 24 hours.)
        - Syllabus details (e.g., Found in 'Course Materials', covers Intro to AI, ML Basics, Deep Learning.)
        - Payment information (e.g., View status in 'Billing', contact finance@scoreazy.com or +1-800-555-0199 for issues.)
        - Certificate issuance (e.g., Issued within 2 weeks of completion if assignments/fees are cleared. Email notification for download.)
        
        Provide helpful and direct answers based on the course context."""),
        ("human", "{user_question}")
    ])

    # Create a Langchain chain to combine prompt, LLM, and output parser
    chain = prompt_template | llm | StrOutputParser()

except ValueError as e:
    print(f"Configuration Error: {e}")
    llm = None # Indicate that LLM setup failed
    chain = None
    initialization_error = str(e)
except Exception as e:
    print(f"An unexpected error occurred during LLM initialization: {e}")
    llm = None
    chain = None
    initialization_error = "Failed to initialize LLM. Check API key and network."


@app.route('/api/generate_response', methods=['POST'])
def generate_response_endpoint():
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({'error': 'No question provided'}), 400

    if chain is None:
        return jsonify({'answer': f"Agent is not initialized due to an error: {initialization_error}. Please check server logs."}), 500

    print(f"Received user question: '{user_question}'")

    try:
        # Invoke the Langchain chain with the user's question
        agent_response_text = chain.invoke({"user_question": user_question})
        print(f"Generated agent response: '{agent_response_text}'")
        return jsonify({'answer': agent_response_text})
    except Exception as e:
        print(f"Error generating response: {e}")
        return jsonify({'answer': "I'm currently experiencing technical difficulties. Please try again later."}), 500

if __name__ == "__main__":
    # To run the Flask server:
    # 1. Ensure you have Flask, Flask-CORS, langchain-google-genai, google-generativeai, and python-dotenv installed.
    # 2. Set your GEMINI_API_KEY in your environment variables or a .env file in this directory.
    # 3. Run this script: python app.py
    # This will start the server, typically on http://127.0.0.1:5000/
    app.run(debug=True, port=5000)