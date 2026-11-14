"""
CAMAS API endpoint for Vercel serverless
"""
import json
import random
import time
from http.server import BaseHTTPRequestHandler


def handler(request: BaseHTTPRequestHandler):
    """Handle POST /api/query requests"""
    
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
        }
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Method not allowed'}),
        }
    
    try:
        body = json.loads(request.body)
        query = body.get('query', '')
        mode = body.get('mode', 'camas')
        
        if not query.strip():
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Query is required'}),
            }
        
        # Estimate complexity from query
        query_lower = query.lower()
        complexity = min(10.0, 2.0 + len(query) / 20.0)
        
        if any(kw in query_lower for kw in ["complex", "analyze", "algorithm", "architecture", "deep", "explain in detail"]):
            complexity = min(10.0, complexity + 3.0)
        if any(kw in query_lower for kw in ["simple", "what is", "define", "short"]):
            complexity = max(2.0, complexity - 2.0)
        
        # Model selection
        baseline_model = "samantha-mistral:latest"  # 7B
        simple_model = "llama3.2:latest"             # 3.2B
        medium_model = "llama3.2:latest"             # 3.2B
        
        if mode == "baseline":
            selected_model = baseline_model
        else:
            if complexity < 3.0:
                selected_model = simple_model
            elif complexity < 7.0:
                selected_model = medium_model
            else:
                selected_model = baseline_model
        
        # Generate realistic metrics (mock data)
        if mode == "baseline":
            response_latency = 3000 + random.randint(-500, 1000)
            response_energy = 0.0000850 + random.uniform(-0.00001, 0.00002)
        else:
            if complexity < 3.0:
                response_latency = 1500 + random.randint(-300, 600)
                response_energy = 0.0000190 + random.uniform(-0.000002, 0.000003)
            elif complexity < 7.0:
                response_latency = 2200 + random.randint(-400, 700)
                response_energy = 0.0000380 + random.uniform(-0.000004, 0.000005)
            else:
                response_latency = 2800 + random.randint(-500, 900)
                response_energy = 0.0000850 + random.uniform(-0.000006, 0.000008)
        
        response_co2 = response_energy * 475
        response_cost = response_energy * 0.12
        
        routing_reason = (
            f"Baseline: always uses {baseline_model}" if mode == "baseline"
            else f"CAMAS: complexity={complexity:.1f}, routed to {selected_model}"
        )
        
        result = {
            "query": query,
            "mode": mode,
            "model": selected_model,
            "complexity": complexity,
            "response": f"Response to: {query}",
            "latency_ms": response_latency,
            "energy_kwh": response_energy,
            "co2_g": response_co2,
            "cost_usd": response_cost,
            "routing_reason": routing_reason,
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(result),
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)}),
        }
