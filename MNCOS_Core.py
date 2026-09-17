from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict
import datetime, uuid

app = FastAPI(title="MNCOS SCU·32 Sovereign Engine", version="1.0.0")

class Scu32Context(BaseModel):
    observation_id: str
    context_vector: str
    historical_trace: List[str]
    governance_boundary: str

class ExecutionRequest(BaseModel):
    action: str
    context: Scu32Context

AUDIT_TRAIL: List[Dict] = []

@app.post("/evaluate")
def evaluate_admissibility(request: ExecutionRequest):
    timestamp = datetime.datetime.utcnow().isoformat()
    audit_id = str(uuid.uuid4())
    ctx, action = request.context, request.action

    if not ctx.historical_trace:
        raise HTTPException(status_code=403, detail="REJECTED - Traceability chain broken.")
    if not ctx.governance_boundary:
        raise HTTPException(status_code=403, detail="REJECTED - Governance boundary undefined.")

    success_msg = f"ADMITTED - Action '{action}' verified."
    AUDIT_TRAIL.append({"audit_id": audit_id, "status": "ADMITTED", "reason": success_msg})
    return {"status": "ADMITTED", "reason": success_msg, "audit_id": audit_id}

@app.get("/audit-trail")
def get_audit_trail():
    return {"total": len(AUDIT_TRAIL), "trail": AUDIT_TRAIL}

@app.get("/health")
def health():
    return {"status": "MNCOS Core is operational 24/7"}
