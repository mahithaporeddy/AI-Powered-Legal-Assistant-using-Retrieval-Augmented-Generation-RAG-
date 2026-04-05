from fastapi import FastAPI
from google import genai
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import search_documents

# import database
from database import SessionLocal, Chat

app = FastAPI()

# allow frontend connection
app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

# Gemini client
client = genai.Client(api_key="AIzaSyBi1nLcBkzrA9L1NCL1SNdWiIssWgsKX8s")


# request format
class ChatRequest(BaseModel):

    user_message: str


@app.get("/")
def home():

    return {"message": "Backend running"}




@app.post("/chat")

def chat(request: ChatRequest):

    # search legal knowledge
    context = search_documents(request.user_message)

    # create prompt using retrieved context
    prompt = f"""

    Answer the question using the legal context below.

    Legal context:
    {context}

    Question:
    {request.user_message}

    """

    # send to Gemini
    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt

    )

    ai_reply = response.text


    # store chat in database
    db = SessionLocal()

    new_chat = Chat(

        user_message=request.user_message,

        ai_response=ai_reply

    )

    db.add(new_chat)

    db.commit()

    db.close()


    return {

        "reply": ai_reply

    }