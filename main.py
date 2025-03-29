import torch
from fastapi import FastAPI
from transformers import BertTokenizer, BertForSequenceClassification
from pathlib import Path
import google.generativeai as genai
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Load BERT Model
MODEL_PATH = Path(r"F:\modelllll\legal_bert_finetuned")
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

# Configure Gemini API
genai.configure(api_key="AIzaSyDrelytnX0j1f5MuPrrF38wQit6l6FWW7s")
MODEL = genai.GenerativeModel("gemini-1.5-flash")

# Initialize FastAPI
app = FastAPI()

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    message: str

# Function to classify the input
def analyze_question(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    
    probs = torch.softmax(outputs.logits, dim=1)[0]
    legal_prob = probs[1].item()  # Probability it's a legal question
    is_legal = legal_prob > 0.3  # Adjusted threshold
    
    return is_legal, legal_prob

# Generate legal response
def generate_legal_response(question):
    response = MODEL.generate_content(
        f"Provide a detailed legal analysis for the following question: '{question}'. "
        "Ensure the response is legally accurate, well-structured, and concise."
    )
    return response.text

# API Route
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    is_legal, confidence = analyze_question(request.message)

    if is_legal:
        response_text = generate_legal_response(request.message)
        return {"response": response_text, "legal": True}
    else:
        return {"response": "I'm sorry, but this does not appear to be a legal question.", "legal": False}

