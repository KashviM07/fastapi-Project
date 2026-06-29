import google.generativeai as genai
from fastapi import HTTPException

genai.configure(
    api_key="AQ.Ab8RN6IdFff9_eEXk1svsPlmOruIuxtnlZRJNrWLhb0rAKP9IA"
)

model = genai.GenerativeModel("gemini-2.5-flash")

"""
def generate_message(conversations):
    try:
        print(conversations)

        history = []

        for convo in conversations[:-1]:
            history.append({
                "role": "user" if convo.role == "user" else "model",
                "parts": [convo.content]
            })

        print("History:", history)

        chat = model.start_chat(history=history)

        response = chat.send_message(conversations[-1].content)

        return response.text

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
"""
from rag import retrieve_context

def generate_message(conversations):

    user_message = conversations[-1].content

    context = retrieve_context(user_message)

    history = []

    for convo in conversations[:-1]:
        history.append({
            "role": "user" if convo.role == "user" else "model",
            "parts": [convo.content]
        })

    chat = model.start_chat(history=history)

    prompt = f"""
    Answer only from this brochure.

    Context:
    {context}

    Question:
    {user_message}

    If the answer is not in the brochure,
    say "Information not available in brochure."
    """

    response = chat.send_message(prompt)

    return response.text