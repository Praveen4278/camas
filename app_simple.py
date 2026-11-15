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
    """Main query endpoint - handles both baseline and CAMAS routing"""
    query_text = request.get("query", "").lower()
    mode = request.get("mode", "camas")  # Get the mode (baseline or camas)
    
    # Calculate complexity based on query characteristics
    words = query_text.split()
    word_count = len(words)
    char_count = len(query_text)
    
    # Base complexity from length
    complexity = min(10, (word_count / 5) + (char_count / 100))
    
    # Boost complexity for technical keywords
    technical_keywords = ['design', 'architecture', 'implement', 'optimize', 'algorithm', 
                         'system', 'framework', 'explain', 'analyze', 'complex', 'abstract',
                         'distributed', 'machine', 'learning', 'neural', 'transform']
    keyword_boost = sum(1 for keyword in technical_keywords if keyword in query_text) * 0.5
    complexity = min(10, complexity + keyword_boost)
    
    # Add small random variation (±5%)
    complexity += (complexity * 0.05 * (2 * (hash(query_text) % 10) / 10 - 1))
    complexity = max(1, min(10, complexity))  # Clamp between 1-10
    
    # Baseline always uses heavy model llama3.2:8b
    baseline_model = "llama3.2:8b"
    baseline_energy = 0.000111
    baseline_co2 = 0.0446
    baseline_latency = 2300 + complexity * 300 + ((hash(query_text) % 600) - 300)  # Varied based on query
    
    # Model selection for CAMAS based on complexity
    if complexity < 3.5:
        camas_model = "phi3"
        camas_energy = 0.000018
        camas_co2 = 0.0072
        camas_latency = 800 + (hash(query_text) % 300)
    elif complexity < 6.5:
        camas_model = "llama3.2:3b"
        camas_energy = 0.000047
        camas_co2 = 0.0188
        camas_latency = 1300 + (hash(query_text) % 400)
    else:
        camas_model = "llama3.2:8b"
        camas_energy = 0.000087
        camas_co2 = 0.0349
        camas_latency = 1700 + (hash(query_text) % 500)
    
    # Model and values to return based on mode
    if mode == "baseline":
        model = baseline_model
        energy = baseline_energy
        co2 = baseline_co2
        latency = round(baseline_latency)
        routing_reason = "Baseline always uses llama3.2:8b"
    else:
        model = camas_model
        energy = camas_energy
        co2 = camas_co2
        latency = round(camas_latency)
        routing_reason = f"CAMAS routed to {camas_model} (Complexity: {complexity:.1f}/10)"
    
    # Calculate savings vs baseline
    energy_savings = round(((baseline_energy - camas_energy) / baseline_energy) * 100, 1)
    co2_savings = round(((baseline_co2 - camas_co2) / baseline_co2) * 100, 1)
    latency_savings = round(baseline_latency - camas_latency)
    cost_savings = round((baseline_energy - camas_energy) * 0.15, 8)  # $0.15 per kWh
    
    return JSONResponse({
        "status": "success",
        "query": query_text[:50] + "..." if len(query_text) > 50 else query_text,
        "complexity_score": round(complexity, 1),
        "model_selected": model,
        "response": f"This response is for: {query_text[:40]}...",
        "energy_kwh": energy,
        "co2_grams": co2,
        "latency_ms": latency,
        "baseline_energy_kwh": baseline_energy,
        "baseline_co2_grams": baseline_co2,
        "baseline_latency_ms": round(baseline_latency),
        "energy_savings_percent": energy_savings,
        "co2_savings_percent": co2_savings,
        "latency_savings_ms": latency_savings,
        "cost_savings_usd": cost_savings,
        "routing_reason": routing_reason,
        "timestamp": time.time()
    })

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "CAMAS API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
