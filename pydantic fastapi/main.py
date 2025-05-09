from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import random
import uuid
from datetime import datetime

app = FastAPI()

class Message(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_message: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ChatResponse(BaseModel):
    bot_response: str
    message_id: uuid.UUID
    timestamp: datetime = Field(default_factory=datetime.now)

# Store conversation history
conversation_history: Dict[uuid.UUID, List[dict]] = {}

# Simplified and organized responses
responses = {
    "greeting": {
        "triggers": ["hello", "hi", "hey", "morning", "afternoon", "evening"],
        "responses": [
            "Hello! How can I help you?",
            "Hi there! What's on your mind?",
            "Hey! Ready to chat!"
        ]
    },
    "farewell": {
        "triggers": ["bye", "goodbye", "see you", "later"],
        "responses": [
            "Goodbye! Take care!",
            "See you later!",
            "Have a great day!"
        ]
    },
    "mood": {
        "triggers": ["how are you", "how's it going", "what's up"],
        "responses": [
            "I'm doing great! How about you?",
            "All good here! How are you today?",
            "I'm wonderful! How's your day going?"
        ]
    }
}

def get_response_type(message: str) -> str:
    message = message.lower()
    for response_type, content in responses.items():
        if any(trigger in message for trigger in content["triggers"]):
            return response_type
    return "general"

@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message):
    if message.id not in conversation_history:
        conversation_history[message.id] = []
    
    conversation_history[message.id].append({
        "role": "user",
        "message": message.user_message,
        "timestamp": message.timestamp
    })

    # Get appropriate response
    response_type = get_response_type(message.user_message)
    if response_type in responses:
        response = random.choice(responses[response_type]["responses"])
    else:
        response = "I understand. Tell me more!"
    
    conversation_history[message.id].append({
        "role": "bot",
        "message": response,
        "timestamp": datetime.now()
    })
    
    return ChatResponse(
        bot_response=response,
        message_id=message.id,
        timestamp=datetime.now()
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the ChatBot API"}

@app.get("/history/{chat_id}")
async def get_chat_history(chat_id: uuid.UUID):
    if chat_id not in conversation_history:
        raise HTTPException(status_code=404, detail="Chat history not found")
    return conversation_history[chat_id]