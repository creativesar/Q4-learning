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

# Enhanced responses based on categories
responses = {
    "greeting": [
        "Hello! How can I help you today?",
        "Hi there! Nice to meet you!",
        "Greetings! How may I assist you?",
    ],
    "farewell": [
        "Goodbye! Have a great day!",
        "See you later! Take care!",
        "Farewell! Hope to chat again soon!",
    ],
    "general": [
        "That's interesting! Tell me more.",
        "I understand. Please continue.",
        "Thanks for sharing that with me!",
    ]
}

@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message):
    # Initialize conversation history for new users
    if message.id not in conversation_history:
        conversation_history[message.id] = []
    
    # Store user message
    conversation_history[message.id].append({
        "role": "user",
        "message": message.user_message,
        "timestamp": message.timestamp
    })

    # Enhanced response logic
    msg_lower = message.user_message.lower()
    
    if any(word in msg_lower for word in ["hello", "hi", "hey"]):
        response = random.choice(responses["greeting"])
    elif any(word in msg_lower for word in ["bye", "goodbye", "see you"]):
        response = random.choice(responses["farewell"])
    elif "how are you" in msg_lower:
        response = "I'm doing great! Thanks for asking. How about you?"
    else:
        response = random.choice(responses["general"])
    
    # Store bot response
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