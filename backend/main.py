from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mentor import generate

app = FastAPI(title="AI Project Mentor API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class Request(BaseModel):
    action: str
    profile: dict
    question: str = ""

@app.get("/")
def health():
    return {"status": "ok", "service": "AI Project Mentor"}

@app.post("/mentor")
def mentor(req: Request):
    return {"result": generate(req.action, req.profile, req.question)}
