import google.generativeai as genai
from django.conf import settings

# API_KEY = os.getenv('GEMINI_API_KEY')
# API_KEY=settings.API_KEY

# We put the key here because when we push the project to github the .env file we don't push it so this is the key
API_KEY="AIzaSyAYvg_TWJFWLt7hJfhWE7HRUdgYSdMeBko"
genai.configure (
    api_key=API_KEY
)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
instruction1 = "You're a healthcare chat assistant, and your mission is to question the user (patient)."
instruction2 = "After every response from the user, ask them detailed questions about their status and health to make it easier for you."
instruction3 = "Once you understand the patient's status, give them the percentage of how much the patient needs to see a doctor. Make the percentage of their health between {} (example: 73%)."
instruction4 = "After diagnosing their status, recommend specialist doctors for them, make the name of the specialist between <>"
instruction5 = "Don't give the patient personalized health assessment because you're not a doctor you're just an assistant"
instruction6 = "Don't ask me lot of questions just one question per response"
instruction7 = "Don't mention that you're the assistant"


def AskGemini(question):
    print(API_KEY)
    response = chat.send_message(instruction1 + instruction2 + instruction3 + instruction4 + instruction5 + instruction6 + question)
    print('\n')
    print(f"Assistant:{response.text}")
    print('\n')
    theReponse=f"Assistant:{response.text}"
    return theReponse