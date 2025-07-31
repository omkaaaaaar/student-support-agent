import json
import requests
import os

# This function simulates the core logic of your AI Agent.
# In a real application, this would be a backend endpoint that receives the user's question.
def generate_agent_response(user_question: str) -> str:
    """
    Generates a response for the Student Support Agent using a large language model.

    Args:
        user_question (str): The question asked by the student.

    Returns:
        str: The AI agent's generated answer.
    """
    print(f"Received user question: '{user_question}'")

    # --- Step 1: Prepare the prompt for the LLM ---
    # The prompt guides the LLM on how to respond.
    # We instruct it to act as a helpful course support agent.
    prompt = f"""
    You are an AI-powered student support agent for an online course.
    Your goal is to answer student questions accurately and concisely based on common course inquiries.
    If you don't know the answer, politely state that you cannot find the information and suggest
    they contact support.

    Common topics include:
    - Course timing/schedule
    - Syllabus details
    - Payment information
    - Certificate issuance

    Student's question: "{user_question}"

    Please provide a helpful and direct answer.
    """

    # --- Step 2: Simulate LLM API Call (using Gemini API structure) ---
    # In a real application, you would make an HTTP POST request to the LLM API endpoint.
    # For this assignment, we are demonstrating the *design* and *logic*.

    # Replace with your actual API key if running this outside a Canvas environment
    # For Canvas, the API key is automatically provided in the fetch call.
    api_key = os.environ.get("GEMINI_API_KEY", "") # Placeholder for actual API key

    # Define the model to use. gemini-2.5-flash-preview-05-20 is a good choice for quick responses.
    model_name = "gemini-2.5-flash-preview-05-20"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    chat_history = []
    chat_history.append({"role": "user", "parts": [{"text": prompt}]})

    payload = {
        "contents": chat_history
    }

    headers = {
        'Content-Type': 'application/json'
    }

    # In a real scenario, you would use a library like `requests` to make the call:
    # try:
    #     response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    #     response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
    #     result = response.json()
    #
    #     if result.get("candidates") and result["candidates"][0].get("content") and \
    #        result["candidates"][0]["content"].get("parts") and \
    #        result["candidates"][0]["content"]["parts"][0].get("text"):
    #         agent_response_text = result["candidates"][0]["content"]["parts"][0]["text"]
    #     else:
    #         agent_response_text = "I apologize, but I couldn't generate a response. Please try again."
    # except requests.exceptions.RequestException as e:
    #     print(f"API call failed: {e}")
    #     agent_response_text = "I'm currently experiencing technical difficulties. Please try again later."

    # --- Placeholder for LLM response (as we are not executing a live API call here) ---
    # For the purpose of this assignment, we'll simulate the LLM's response based on keywords,
    # just like the JavaScript in the frontend UI.
    agent_response_text = "I'm sorry, I couldn't find an answer to that specific question. Please try rephrasing or check the course FAQ."
    if "syllabus" in user_question.lower():
        agent_response_text = "The detailed syllabus can be found in the 'Course Materials' section of your student portal. It covers modules on Introduction to AI, Machine Learning Basics, and Deep Learning Concepts."
    elif "timing" in user_question.lower() or "schedule" in user_question.lower():
        agent_response_text = "Live sessions are held every Monday and Wednesday at 5 PM PST. Recordings are available within 24 hours in the 'Lecture Recordings' section."
    elif "payment" in user_question.lower():
        agent_response_text = "You can view your payment status and options in the 'Billing' section of your student dashboard. For any issues, please contact our finance department at finance@scoreazy.com or call +1-800-555-0199."
    elif "certificate" in user_question.lower():
        agent_response_text = "Certificates are issued within 2 weeks of course completion, provided all assignments are submitted and fees are cleared. You will receive an email notification to download your certificate."
    elif "contact" in user_question.lower() or "support" in user_question.lower():
        agent_response_text = "You can contact our support team via email at support@scoreazy.com or by calling +1-800-555-0199 during business hours (9 AM - 5 PM PST, Monday-Friday)."

    print(f"Generated agent response: '{agent_response_text}'")
    return agent_response_text

# Example of how you would use this function:
if __name__ == "__main__":
    test_questions = [
        "What is the course syllabus?",
        "When are the live sessions?",
        "How do I check my payment status?",
        "When will I get my certificate?",
        "I need to contact support.",
        "Can you tell me about the homework?", # This will get the fallback message
    ]

    for question in test_questions:
        print(f"\n--- Testing with question: '{question}' ---")
        response = generate_agent_response(question)
        print(f"Agent's Answer: {response}")

