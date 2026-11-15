import axios from 'axios'

// API client for CAMAS - use environment variable or fallback to localhost
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
console.log(`[API] Using base URL: ${baseURL}`)

const client = axios.create({
  baseURL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Mock data generator - matches backend logic exactly
function generateMockResult(query, mode) {
  const queryLower = query.toLowerCase()
  
  // Calculate complexity based on query characteristics (matches backend)
  const words = queryLower.split(' ')
  const wordCount = words.length
  const charCount = queryLower.length
  
  // Base complexity from length
  let complexity = Math.min(10, (wordCount / 5) + (charCount / 100))
  
  // Boost complexity for technical keywords (matches backend)
  const technicalKeywords = ['design', 'architecture', 'implement', 'optimize', 'algorithm', 
                             'system', 'framework', 'explain', 'analyze', 'complex', 'abstract',
                             'distributed', 'machine', 'learning', 'neural', 'transform']
  const keywordBoost = technicalKeywords.filter(k => queryLower.includes(k)).length * 0.5
  complexity = Math.min(10, complexity + keywordBoost)
  
  // Add small random variation (±5%)
  const hashValue = queryLower.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  complexity += (complexity * 0.05 * (2 * ((hashValue % 10) / 10) - 1))
  complexity = Math.max(1, Math.min(10, complexity))
  
  // Baseline always uses llama3.2:8b
  const baselineModel = 'llama3.2:8b'
  const baselineEnergy = 0.000111
  const baselineCo2 = 0.0446
  const baselineLatency = 2300 + complexity * 300 + ((hashValue % 600) - 300)
  
  // Model selection for CAMAS based on complexity (matches backend thresholds)
  let camasModel, camasEnergy, camasCo2, camasLatency
  if (complexity < 3.5) {
    camasModel = 'phi3'
    camasEnergy = 0.000018
    camasCo2 = 0.0072
    camasLatency = 800 + (hashValue % 300)
  } else if (complexity < 6.5) {
    camasModel = 'llama3.2:3b'
    camasEnergy = 0.000047
    camasCo2 = 0.0188
    camasLatency = 1300 + (hashValue % 400)
  } else {
    camasModel = 'llama3.2:8b'
    camasEnergy = 0.000087
    camasCo2 = 0.0349
    camasLatency = 1700 + (hashValue % 500)
  }
  
  // Select based on mode
  const selectedModel = mode === 'baseline' ? baselineModel : camasModel
  const selectedEnergy = mode === 'baseline' ? baselineEnergy : camasEnergy
  const selectedCo2 = mode === 'baseline' ? baselineCo2 : camasCo2
  const selectedLatency = mode === 'baseline' ? baselineLatency : camasLatency
  
  // Calculate savings (CAMAS vs baseline)
  const energySavings = Math.round(((baselineEnergy - camasEnergy) / baselineEnergy) * 1000) / 10
  const co2Savings = Math.round(((baselineCo2 - camasCo2) / baselineCo2) * 1000) / 10
  const latencySavings = Math.round(baselineLatency - camasLatency)
  const costSavings = Math.round((baselineEnergy - camasEnergy) * 0.15 * 100000000) / 100000000
  
  return {
    query: query,
    mode: mode,
    model_selected: selectedModel,
    complexity_score: Math.round(complexity * 10) / 10,
    response: `This response demonstrates intelligent ${mode === 'baseline' ? 'baseline' : 'CAMAS'} routing.`,
    latency_ms: Math.round(selectedLatency),
    energy_kwh: selectedEnergy,
    co2_grams: selectedCo2,
    cost_usd: selectedEnergy * 0.15,
    baseline_energy_kwh: baselineEnergy,
    baseline_co2_grams: baselineCo2,
    baseline_latency_ms: Math.round(baselineLatency),
    energy_savings_percent: energySavings,
    co2_savings_percent: co2Savings,
    latency_savings_ms: latencySavings,
    cost_savings_usd: costSavings,
    routing_reason: mode === 'baseline' 
      ? 'Baseline always uses llama3.2:8b'
      : `CAMAS routed to ${camasModel} (Complexity: ${complexity.toFixed(1)}/10)`,
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
