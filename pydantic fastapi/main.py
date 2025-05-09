from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import random
import uuid

app = FastAPI()

class Message(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_message: str

class ChatResponse(BaseModel):
    bot_response: str

# Store some simple responses
responses = [
    "Hello! How can I help you today?",
    "That's interesting! Tell me more.",
    "I understand. Please continue.",
    "Thanks for sharing that with me!",
    "I'm here to chat with you!",
]

@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message):
    # Simple logic to generate responses
    if "hello" in message.user_message.lower():
        response = "Hi there! How are you?"
    elif "how are you" in message.user_message.lower():
        response = "I'm doing great! Thanks for asking."
    elif "bye" in message.user_message.lower():
        response = "Goodbye! Have a great day!"
    else:
        response = random.choice(responses)
    
    return ChatResponse(bot_response=response)

@app.get("/")
async def root():
    return {"message": "Welcome to the ChatBot API"}