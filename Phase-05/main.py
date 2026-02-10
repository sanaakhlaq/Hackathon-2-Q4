import asyncio
import json
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from pydantic import BaseModel
from aiokafka import AIOKafkaProducer

# --- 1. Imports from your local files ---
from models import init_db, engine
from auth import signup_user, get_user_by_email, verify_password, create_access_token
from agent import run_agent  # Aapki agent.py se function connect kar rahe hain

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to hold the Kafka producer instance
kafka_producer = None

# --- 2. Application Lifecycle (Lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global kafka_producer
    logger.info("Server Starting: Initializing Database and Kafka Producer...")
    try:
        init_db()  # Tables create karega
        logger.info("Database initialized successfully.")
        
        # Initialize Kafka producer
        kafka_producer = AIOKafkaProducer(bootstrap_servers='kafka:9092')
        await kafka_producer.start()
        logger.info("Kafka producer initialized successfully.")
    except Exception as e:
        logger.error(f"Initialization error: {e}")
    yield
    logger.info("Server Shutting down...")
    if kafka_producer:
        await kafka_producer.stop()
        logger.info("Kafka producer stopped.")

# --- 3. FastAPI Initialization ---
app = FastAPI(
    title="Agentic Todo System",
    description="Backend with AI Agent Integration",
    version="3.0.0",
    lifespan=lifespan
)

# --- 4. Middleware Setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# --- 5. Helper Functions ---
async def send_kafka_event(topic: str, message: dict):
    """Send an event to Kafka topic"""
    global kafka_producer
    if kafka_producer:
        try:
            msg_value = json.dumps(message).encode('utf-8')
            await kafka_producer.send_and_wait(topic, msg_value)
            logger.info(f"Event sent to Kafka topic '{topic}': {message}")
        except Exception as e:
            logger.error(f"Failed to send event to Kafka: {e}")

# --- 6. Pydantic Schemas for Validation ---
class UserSignup(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class AIChatRequest(BaseModel):
    prompt: str
    conversation_id: int = 1

# --- 6. Routes ---

@app.get("/")
async def root():
    return {"message": "Phase 3 Backend is LIVE!", "docs": "/docs"}

# --- Auth Routes ---
@app.post("/signup")
def signup(data: UserSignup):
    try:
        user = signup_user(data.name, data.email, data.password)
        return {"message": "User registered!", "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login")
def login(data: UserLogin):
    user = get_user_by_email(data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# --- AI Agent Route (The Heart of Phase 3) ---
@app.post("/chat-with-ai")
async def chat_with_ai(request: AIChatRequest):
    """
    User prompts like 'Add a task to buy bread' will be processed by Groq AI
    through the agent.py logic.
    """
    try:
        # Agent ko prompt bhejna
        response = run_agent(request.prompt, request.conversation_id)
        
        # Check if the response indicates a task was added and send Kafka event
        prompt_lower = request.prompt.lower()
        if any(keyword in prompt_lower for keyword in ["add ", "create ", "new task", "task to"]):
            # Send task-added event to Kafka
            task_event = {
                "event_type": "task-added",
                "prompt": request.prompt,
                "response": response,
                "conversation_id": request.conversation_id
            }
            await send_kafka_event("task-added", task_event)
        
        return {"ai_response": response}
    except Exception as e:
        logger.error(f"Agent Error: {e}")
        raise HTTPException(status_code=500, detail="AI Agent is having trouble processing that.")

# --- 7. Run Server ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)