"""
CAMAS Simple Mock API - Lightweight version for demo
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import time

app = FastAPI(title="CAMAS API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "CAMAS API v1.0.0", "status": "online"}

@app.post("/orchestrate")
def orchestrate(request: dict):
    """Mock orchestration endpoint with intelligent routing"""
    query = request.get("query", "").lower()
    
    # Simple complexity scoring
    complexity = min(10, len(query.split()) // 2 + len(query) // 50)
    
    # Model selection based on complexity
    if complexity < 4:
        model = "phi3"
        energy = 0.000018
        co2 = 0.0072
    elif complexity < 8:
        model = "llama3.2:3b"
        energy = 0.000047
        co2 = 0.0188
    else:
        model = "llama3.2:8b"
        energy = 0.000087
        co2 = 0.0349
    
    return JSONResponse({
        "status": "success",
        "query": query[:50] + "..." if len(query) > 50 else query,
        "complexity_score": complexity,
        "model_selected": model,
        "response": "This is a mock response from CAMAS demonstrating intelligent LLM routing.",
        "energy_kwh": energy,
        "co2_grams": co2,
        "latency_ms": 1500 + complexity * 100,
        "baseline_energy_kwh": 0.000111,
        "baseline_co2_grams": 0.0446,
        "energy_savings_percent": round(((0.000111 - energy) / 0.000111) * 100, 1),
        "timestamp": time.time()
    })

@app.post("/query")
def query(request: dict):
    """Main query endpoint - same as orchestrate"""
    query_text = request.get("query", "").lower()
    
    # Simple complexity scoring
    complexity = min(10, len(query_text.split()) // 2 + len(query_text) // 50)
    
    # Model selection based on complexity
    if complexity < 4:
        model = "phi3"
        energy = 0.000018
        co2 = 0.0072
    elif complexity < 8:
        model = "llama3.2:3b"
        energy = 0.000047
        co2 = 0.0188
    else:
        model = "llama3.2:8b"
        energy = 0.000087
        co2 = 0.0349
    
    return JSONResponse({
        "status": "success",
        "query": query_text[:50] + "..." if len(query_text) > 50 else query_text,
        "complexity_score": complexity,
        "model_selected": model,
        "response": "This is a mock response from CAMAS demonstrating intelligent LLM routing.",
        "energy_kwh": energy,
        "co2_grams": co2,
        "latency_ms": 1500 + complexity * 100,
        "baseline_energy_kwh": 0.000111,
        "baseline_co2_grams": 0.0446,
        "energy_savings_percent": round(((0.000111 - energy) / 0.000111) * 100, 1),
        "timestamp": time.time()
    })

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "CAMAS API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
