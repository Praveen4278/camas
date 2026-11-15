import axios from 'axios'

// API client for CAMAS
const client = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Mock data generator using only your 3 models
function generateMockResult(query, mode) {
  const queryLower = query.toLowerCase()
  
  // Complexity scoring based on query length and keywords
  let complexity = Math.min(10.0, (query.split(' ').length / 3) + (query.length / 100))
  
  // Boost for complex keywords
  if (queryLower.includes('design') || queryLower.includes('architecture') || 
      queryLower.includes('complex') || queryLower.includes('explain') ||
      queryLower.includes('implement') || queryLower.includes('optimize')) {
    complexity = Math.min(10, complexity + 2)
  }
  
  // Model selection
  let model, energy, co2
  if (mode === 'baseline') {
    model = 'llama3.2:8b'
    energy = 0.000111
    co2 = 0.0446
  } else {
    // CAMAS routing
    if (complexity < 4) {
      model = 'phi3'
      energy = 0.000018
      co2 = 0.0072
    } else if (complexity < 8) {
      model = 'llama3.2:3b'
      energy = 0.000047
      co2 = 0.0188
    } else {
      model = 'llama3.2:8b'
      energy = 0.000087
      co2 = 0.0349
    }
  }
  
  return {
    query: query,
    mode: mode,
    model: model,
    complexity: complexity,
    response: `This response demonstrates intelligent ${mode === 'baseline' ? 'baseline' : 'CAMAS'} routing.`,
    latency_ms: 1500 + (complexity * 150) + (Math.random() * 500),
    energy_kwh: energy,
    co2_g: co2,
    cost_usd: energy * 0.15,
    routing_reason: mode === 'baseline' 
      ? 'Baseline always uses llama3.2:8b'
      : `CAMAS routed to ${model} (Complexity: ${complexity.toFixed(1)}/10)`,
  }
}

export default client

export const API = {
  // Execute query - tries backend first, falls back to mock
  executeQuery: async (query, mode = 'camas') => {
    try {
      console.log(`[API] Attempting to call backend for ${mode} query...`)
      const response = await client.post('/query', { query, mode })
      console.log(`[API] Backend response received:`, response)
      
      // Extract and map backend response to expected format
      const data = response.data || response
      const mapped = {
        query: data.query || query,
        mode: mode,
        model: data.model_selected || data.model || (mode === 'baseline' ? 'llama3.2:8b' : 'phi3'),
        complexity: data.complexity_score || data.complexity || 5,
        response: data.response || '',
        latency_ms: data.latency_ms || 1500,
        energy_kwh: data.energy_kwh || 0.00005,
        co2_g: data.co2_grams || data.co2_g || 0.02,
        cost_usd: data.cost_usd || (data.energy_kwh * 0.15) || 0.000075,
        baseline_latency_ms: data.baseline_latency_ms || 2500,
        energy_savings_percent: data.energy_savings_percent !== undefined ? data.energy_savings_percent : 0,
        co2_savings_percent: data.co2_savings_percent !== undefined ? data.co2_savings_percent : 0,
        latency_savings_ms: data.latency_savings_ms !== undefined ? data.latency_savings_ms : 0,
        cost_savings_usd: data.cost_savings_usd !== undefined ? data.cost_savings_usd : 0,
        routing_reason: data.routing_reason || (mode === 'baseline' 
          ? 'Baseline always uses llama3.2:8b'
          : `CAMAS routed to ${data.model_selected}`),
      }
      
      console.log(`[API] Mapped response for mode="${mode}":`, {
        energy_savings_percent: mapped.energy_savings_percent,
        model: mapped.model,
        complexity: mapped.complexity,
        raw_data: data
      })
      return mapped
    } catch (error) {
      console.warn(`[API] Backend failed (${error.message}), using mock data`)
      // Simulate network delay
      return new Promise((resolve) => {
        setTimeout(() => {
          const mock = generateMockResult(query, mode)
          console.log(`[API] Generated mock result:`, mock)
          resolve(mock)
        }, 800)
      })
    }
  },

  // Health check
  health: async () => {
    try {
      const response = await client.get('/health')
      return response.data || response
    } catch {
      return { status: 'unavailable' }
    }
  },
}
