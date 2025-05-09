from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, UTC
from uuid import uuid4


# Create a FastAPI instance
app = FastAPI(
    title="FastAPI with Pydantic Example Practice",
    description="An example of using FastAPI with Pydantic for Practice.",
    version="0.1.0",
)


# Define a Pydantic model for metadata
class Metadata(BaseModel):
    
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(tz=UTC) # generate current UTC time
        )
    
    session_id: str = Field(
        default_factory=lambda: str(uuid4()) # genrate UUID
        ) 
    
    
# Define a Pydantic model for incoming user messages
class Message(BaseModel):
    user_id: str
    text: str
    metadata: Metadata 
    tags: list[str] | None = None
    
    
# Define a Pydantic model for the response
class Response(BaseModel):
    user_id: str
    reply: str
    metadata: Metadata
    
    
    
# Get meathod for Root endpoint returning a welcome message
@app.get("/")
async def root():
    
    return {
        "message": "Welcome to the FastAPI with Pydantic Example!"
        }


# Get endpoint to retrieve user information based on user_id
@app.get("/user/{user_id}")
async def get_user(user_id: str, role: str | None = None):
    
    # create a simple user data dictionary
    user_data = {
        "user_id": user_id,
        "role": role if role else "guest",
    }
    
    # REturn user data
    return user_data



# Post endpoint to handle api conversation
@app.post("/chat/", response_model=Response)

async def chat(message: Message):
    
    # Check if message text is empty after stripping whitespace
    if not message.text.strip():
        
        # If the message text is empty, raise an HTTPException
        raise HTTPException(
            status_code=400, 
            detail="Message text cannot be empty."
            )
    
    # Create a simple reply acknowledging the message
    reply_text = f"Hello, {message.user_id}! \nReceived your message: {message.text}"
    
    # return a response object with user_id, reply, and metadata
    return Response(
        user_id=message.user_id,
        reply=reply_text,
        metadata=Metadata()
    )