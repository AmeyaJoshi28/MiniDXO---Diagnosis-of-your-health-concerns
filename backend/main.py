from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agents import ResearcherAgent, OrchestratorAgent, InterviewerAgent

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents
res = ResearcherAgent()
orch = OrchestratorAgent()
inter = InterviewerAgent()

class ChatInput(BaseModel):
    message: str

@app.post("/reset")
async def reset_session():
    """Resets the agent states for a new patient."""
    global orch, res, inter
    res = ResearcherAgent()
    orch = OrchestratorAgent()
    inter = InterviewerAgent()
    return {"status": "Agent memory cleared"}

@app.post("/chat")
async def handle_chat(data: ChatInput):
    # 1. Fetch relevant medical data based on input
    evidence = res.fetch_evidence(data.message)
    
    # 2. Update the confidence bars (beliefs)
    status = orch.update_beliefs(evidence, data.message)
    
    # 3. Get next question or final diagnosis
    reply, why, force_finish = inter.generate_question(orch.beliefs, res.db, orch.history, orch.asked_questions)

    if status == "DIAGNOSE" or force_finish:
        top_name = max(orch.beliefs, key=orch.beliefs.get)
        disease_entry = next((item for item in res.db.values() if item["name"] == top_name), None)
        
        # PROMPT: Forcing Gemini 3 to provide a Clinical Summary
        prompt = (
            f"SYSTEM: You are a Medical Diagnostic AI.\n"
            f"PATIENT DATA: {orch.history}\n"
            f"LIKELY CONDITION: {top_n}\n"
            f"TASK: Provide a clinical summary in HTML format.\n"
            f"RULES:\n"
            f"- Use <h3> for the title.\n"
            f"- Use <strong> for labels like 'Condition:' or 'Next Steps:'.\n"
            f"- Use <p> for paragraphs.\n"
            f"- DO NOT USE MARKDOWN (no asterisks ** or ***).\n"
            f"- Explain why the symptoms suggest {top_n} and give a disclaimer."
        )
        
        diagnosis_text = inter.ask_gemini(prompt)
        reply = f"<h3>Diagnostic Summary</h3><p>{diagnosis_text}</p>"
        current_reasoning = f"Confidence threshold met for {top_name}."
    else:
        current_reasoning = f"{orch.monologue}<br/><strong>Step:</strong> {why}"

    return {
        "reply": reply, 
        "reasoning": current_reasoning, 
        "confidence": orch.beliefs
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)